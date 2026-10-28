// Public contribution records are explicit links, never inferred from old text.
export const CONTRIBUTION_TYPES = Object.freeze({
  source: 'Source contribution',
  correction: 'Correction or challenge',
  reproduction: 'Reproduction report',
  review: 'Independent review',
  idea: 'Evidence proposal',
  archived_result: 'Historical task result',
});

export const CONTRIBUTION_STATUSES = Object.freeze({
  submitted: 'Awaiting project review',
  in_review: 'In project review',
  needs_work: 'More evidence requested',
  accepted: 'Accepted into the project record',
  negative_result: 'Reviewed negative result',
  rejected: 'Not accepted',
});

export const CONTRIBUTION_LICENSES = Object.freeze(['UNSPECIFIED', 'CC-BY-4.0', 'CC0-1.0']);
const currentContributionTypes = new Set(['source', 'correction', 'reproduction', 'review', 'idea']);

/** Validate a new structured brief, or preserve the older body-only intake. */
export function validateContributionInput(form) {
  const read = (key, max, required = false) => {
    const raw = typeof form?.get === 'function' ? form.get(key) : form?.[key];
    if (raw !== undefined && raw !== null && typeof raw !== 'string') throw new Error('Use text for ' + key + '.');
    const value = (raw || '').trim();
    if (value.length > max) throw new Error(key + ' is too long (maximum ' + max + ' characters).');
    if (required && !value) throw new Error('Add ' + key + ' to your contribution.');
    return value;
  };
  const mission = read('mission', 40, true);
  const format = read('format', 40);
  if (format && format !== 'contribution-v1') throw new Error('Unknown contribution format.');
  const structured = format === 'contribution-v1';
  const body = read('body', structured ? 24000 : 40000, true);
  if (body.length < 20) throw new Error('Add a substantive contribution and its evidence (at least 20 characters).');
  if (!currentContributionTypes.has(mission) && (structured || !/^LA-M\d{3}$/.test(mission))) {
    throw new Error('Choose a valid contribution type.');
  }
  // Legacy callers do not implicitly grant a license or assert structured provenance.
  if (!structured) return {
    structured: false, mission, body, title: '', target: '', sources: '', method: '',
    uncertainty: 'Not stated', exposure: 'Not declared', credit: '', license: 'UNSPECIFIED', relatedId: null,
  };
  const title = read('title', 180, true);
  const target = read('target', 1000, ['correction', 'reproduction', 'review'].includes(mission));
  const sources = read('sources', 4000, true);
  const method = read('method', 8000, ['reproduction', 'review'].includes(mission));
  const uncertainty = read('uncertainty', 4000) || 'Not stated';
  const exposure = read('exposure', 4000) || 'Not declared';
  const credit = read('credit', 1000);
  const license = read('license', 40) || 'UNSPECIFIED';
  if (!CONTRIBUTION_LICENSES.includes(license)) throw new Error('Choose a supported license for your original contribution.');
  if (read('rights', 10) !== 'yes') throw new Error('Confirm that your original text and references are safe to share.');
  const relatedId = read('relatedId', 128) || read('related_id', 128) || null;
  if (relatedId && !/^[A-Za-z0-9_-]{1,128}$/.test(relatedId)) throw new Error('Use a valid related contribution ID.');
  return {structured, mission, body, title, target, sources, method, uncertainty, exposure, credit, license, relatedId};
}

/** Include this statement in the same database batch as the submission and post. */
export function insertContributionRecord(db, submissionId, postId, data, handle) {
  const title = data.title || (currentContributionTypes.has(data.mission)
    ? CONTRIBUTION_TYPES[data.mission]
    : 'Historical task result · ' + data.mission);
  return db.q(`INSERT INTO contribution_records
    (id,post_id,title,target,sources,method,uncertainty,exposure,credit,license,related_id)
    VALUES(?,?,?,?,?,?,?,?,?,?,?)`,
  submissionId, postId, title, data.target || '', data.sources || '', data.method || '',
  data.uncertainty || 'Not stated', data.exposure || 'Not declared', data.credit || handle,
  data.license || 'UNSPECIFIED', data.relatedId || null);
}

// A hidden ancestor also removes dependent contributions from this public view.
// UNION (not UNION ALL) bounds traversal if a malformed cycle ever reaches storage.
export const CONTRIBUTION_VISIBILITY_CTE = `WITH RECURSIVE visible_contributions(id) AS (
  SELECT r.id FROM contribution_records r
  INNER JOIN submissions s ON s.id=r.id
  INNER JOIN posts p ON p.id=r.post_id AND p.user=s.user
  WHERE p.hidden=0 AND p.parent IS NULL AND r.related_id IS NULL
  UNION
  SELECT r.id FROM contribution_records r
  INNER JOIN visible_contributions v ON r.related_id=v.id
  INNER JOIN submissions s ON s.id=r.id
  INNER JOIN posts p ON p.id=r.post_id AND p.user=s.user
  WHERE p.hidden=0 AND p.parent IS NULL
)`;
const publicContributionSelect = `SELECT r.id,s.mission,r.title,s.body,s.created,s.handle,s.status,s.note,s."commit" AS reviewed_reference,
  r.post_id,r.target,r.sources,r.method,r.uncertainty,r.exposure,r.credit,r.license,r.related_id,p.closed
  FROM contribution_records r
  INNER JOIN submissions s ON s.id=r.id
  INNER JOIN posts p ON p.id=r.post_id
  WHERE r.id IN (SELECT id FROM visible_contributions)`;

function contributionPublicRecord(row, origin = '') {
  const base = typeof origin === 'string' ? origin.replace(/\/$/, '') : '';
  return {
    id: row.id, mission: row.mission,
    type: currentContributionTypes.has(row.mission) ? row.mission : 'archived_result',
    title: row.title, body: row.body, created: row.created, handle: row.handle,
    status: row.status, note: row.note || '', commit: row.reviewed_reference || null,
    postId: row.post_id, relatedId: row.related_id || null,
    fields: {
      target: row.target, sources: row.sources, method: row.method,
      uncertainty: row.uncertainty, exposure: row.exposure, credit: row.credit, license: row.license,
    },
    url: base + '/contributions/' + encodeURIComponent(row.id),
    discussionUrl: base + '/threads/' + encodeURIComponent(row.post_id),
    closed: !!row.closed,
  };
}

async function addContributionDetails(db, items) {
  if (!items.length) return items;
  const ids = items.map(item => item.id), placeholders = ids.map(() => '?').join(',');
  const [replies, reviews] = await Promise.all([
    db.all(`SELECT r.id AS contribution_id,p.id,p.parent,p.handle,p.body,p.created
      FROM posts p INNER JOIN contribution_records r ON r.post_id=p.parent
      WHERE r.id IN (${placeholders}) AND p.hidden=0 ORDER BY p.created ASC,p.id ASC`, ...ids),
    db.all(`SELECT m.target AS contribution_id,m.id,m.action,m.note,m.created,p.handle
      FROM moderation m LEFT JOIN profiles p ON p.id=m.actor
      WHERE m.target IN (${placeholders}) AND m.action IN ('review:submitted','review:in_review','review:needs_work','review:accepted','review:negative_result','review:rejected')
      ORDER BY m.created ASC,m.id ASC`, ...ids),
  ]);
  const byId = new Map(items.map(item => {
    item.replies = []; item.reviewHistory = [];
    return [item.id, item];
  }));
  for (const reply of replies) byId.get(reply.contribution_id)?.replies.push({
    id: reply.id, parent: reply.parent, handle: reply.handle, body: reply.body, created: reply.created,
  });
  for (const review of reviews) byId.get(review.contribution_id)?.reviewHistory.push({
    id: review.id, status: review.action.slice(7), note: review.note, created: review.created,
    handle: review.handle || 'Project steward',
  });
  return items;
}

export async function getPublicContribution(db, contributionId, {origin = '', includeDetails = true} = {}) {
  if (typeof contributionId !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(contributionId)) return null;
  const row = await db.first(`${CONTRIBUTION_VISIBILITY_CTE} ${publicContributionSelect} AND r.id=?`, contributionId);
  if (!row) return null;
  const item = contributionPublicRecord(row, origin);
  if (includeDetails) await addContributionDetails(db, [item]);
  return item;
}

function encodeContributionCursor(item) {
  return btoa(JSON.stringify([item.created, item.id])).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function decodeContributionCursor(cursor) {
  if (!cursor) return null;
  try {
    if (typeof cursor !== 'string' || !/^[A-Za-z0-9_-]{1,512}$/.test(cursor)) throw new Error();
    const value = JSON.parse(atob(cursor.replace(/-/g, '+').replace(/_/g, '/')));
    if (!Array.isArray(value) || value.length !== 2 || !Number.isSafeInteger(value[0]) || value[0] < 0 ||
      typeof value[1] !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(value[1])) throw new Error();
    return value;
  } catch { throw new Error('Invalid contribution cursor. Start again from the first page.'); }
}

/** Cursor order is stable when several contributors submit in the same millisecond. */
export async function listPublicContributions(db, options = {}) {
  const {type = '', status = '', query = options.q || '', cursor = '', origin = '', includeDetails = false, relatedId = ''} = options;
  if (type && !Object.hasOwn(CONTRIBUTION_TYPES, type)) throw new Error('Unknown contribution type filter.');
  if (status && !Object.hasOwn(CONTRIBUTION_STATUSES, status)) throw new Error('Unknown contribution status filter.');
  if (typeof query !== 'string' || query.length > 160) throw new Error('Keep the contribution search to 160 characters.');
  if (relatedId && (typeof relatedId !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(relatedId))) throw new Error('Use a valid related contribution ID.');
  const requested = options.limit === undefined ? 20 : Number(options.limit);
  if (!Number.isInteger(requested) || requested < 1) throw new Error('Use a positive whole number for the page size.');
  const limit = Math.min(requested, includeDetails ? 100 : 50);
  const after = decodeContributionCursor(cursor), conditions = [], args = [];
  if (type === 'archived_result') conditions.push("s.mission NOT IN ('source','correction','reproduction','review','idea')");
  else if (type) { conditions.push('s.mission=?'); args.push(type); }
  if (status) { conditions.push('s.status=?'); args.push(status); }
  if (relatedId) { conditions.push('r.related_id=?'); args.push(relatedId); }
  if (query.trim()) {
    const pattern = '%' + query.trim().replace(/[\\%_]/g, '\\$&') + '%';
    conditions.push("(r.title LIKE ? ESCAPE '\\' OR s.body LIKE ? ESCAPE '\\' OR r.target LIKE ? ESCAPE '\\' OR r.sources LIKE ? ESCAPE '\\')");
    args.push(pattern, pattern, pattern, pattern);
  }
  if (after) { conditions.push('(s.created<? OR (s.created=? AND r.id<?))'); args.push(after[0], after[0], after[1]); }
  const rows = await db.all(`${CONTRIBUTION_VISIBILITY_CTE} ${publicContributionSelect}
    ${conditions.length ? ' AND ' + conditions.join(' AND ') : ''}
    ORDER BY s.created DESC,r.id DESC LIMIT ?`, ...args, limit + 1);
  const items = rows.slice(0, limit).map(row => contributionPublicRecord(row, origin));
  if (includeDetails) await addContributionDetails(db, items);
  return {schemaVersion: 1, items, nextCursor: rows.length > limit ? encodeContributionCursor(items.at(-1)) : null};
}

/** Direct responses are ordinary contributions, with the same public visibility. */
export async function listContributionResponses(db, contributionId, {origin = ''} = {}) {
  if (typeof contributionId !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(contributionId)) return [];
  return (await listPublicContributions(db, {relatedId: contributionId, limit: 50, origin})).items;
}

/** Machine-readable contract for the paginated public read/export response. */
export function contributionSchema() {
  const text = {type: 'string'}, nullableText = {type: ['string', 'null']}, timestamp = {type: 'integer', minimum: 0};
  return {
    $schema: 'https://json-schema.org/draft/2020-12/schema',
    title: 'Linear A public contribution export v1', type: 'object',
    description: 'A public, paginated research record. Contributions are not reviewed findings unless an explicit project disposition and reviewed reference say so. Licenses apply only to the contributor’s own original text; third-party sources retain their rights.',
    required: ['schemaVersion', 'items', 'nextCursor'],
    properties: {
      schemaVersion: {const: 1}, items: {type: 'array', items: {$ref: '#/$defs/contribution'}}, nextCursor: nullableText,
      exportedAt: {type: 'string', format: 'date-time'}, origin: text, licenseNotice: text,
    },
    additionalProperties: false,
    $defs: {
      contribution: {
        type: 'object', additionalProperties: false,
        required: ['id', 'mission', 'type', 'title', 'body', 'created', 'handle', 'status', 'note', 'commit', 'postId', 'relatedId', 'fields', 'url', 'discussionUrl', 'closed'],
        properties: {
          id: text, mission: text, type: {enum: Object.keys(CONTRIBUTION_TYPES)}, title: text, body: text, created: timestamp,
          handle: text, status: {enum: Object.keys(CONTRIBUTION_STATUSES)}, note: text, commit: nullableText,
          postId: text, relatedId: nullableText, url: text, discussionUrl: text, closed: {type: 'boolean'},
          fields: {
            type: 'object', additionalProperties: false,
            required: ['target', 'sources', 'method', 'uncertainty', 'exposure', 'credit', 'license'],
            properties: {target: text, sources: text, method: text, uncertainty: text, exposure: text, credit: text, license: {enum: CONTRIBUTION_LICENSES}},
          },
          replies: {type: 'array', items: {$ref: '#/$defs/reply'}},
          reviewHistory: {type: 'array', items: {$ref: '#/$defs/review'}},
        },
      },
      reply: {
        type: 'object', additionalProperties: false, required: ['id', 'parent', 'handle', 'body', 'created'],
        properties: {id: text, parent: text, handle: text, body: text, created: timestamp},
      },
      review: {
        type: 'object', additionalProperties: false, required: ['id', 'status', 'note', 'created', 'handle'],
        properties: {id: text, status: {enum: Object.keys(CONTRIBUTION_STATUSES)}, note: text, created: timestamp, handle: text},
      },
    },
  };
}
