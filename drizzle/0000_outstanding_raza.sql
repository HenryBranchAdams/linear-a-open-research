CREATE TABLE `claim_events` (
	`id` text PRIMARY KEY NOT NULL,
	`mission` text NOT NULL,
	`user` text NOT NULL,
	`kind` text NOT NULL,
	`created` integer NOT NULL,
	`note` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `claims_user_created` ON `claim_events` (`user`,`created`);--> statement-breakpoint
CREATE TABLE `moderation` (
	`id` text PRIMARY KEY NOT NULL,
	`target` text NOT NULL,
	`actor` text NOT NULL,
	`action` text NOT NULL,
	`note` text NOT NULL,
	`created` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `posts` (
	`id` text PRIMARY KEY NOT NULL,
	`scope` text NOT NULL,
	`parent` text,
	`user` text NOT NULL,
	`handle` text NOT NULL,
	`title` text NOT NULL,
	`body` text NOT NULL,
	`created` integer NOT NULL,
	`hidden` integer DEFAULT 0 NOT NULL,
	`closed` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE INDEX `posts_scope_created` ON `posts` (`scope`,`created`);--> statement-breakpoint
CREATE INDEX `posts_user_created` ON `posts` (`user`,`created`);--> statement-breakpoint
CREATE TABLE `profiles` (
	`id` text PRIMARY KEY NOT NULL,
	`handle` text NOT NULL,
	`role` text DEFAULT 'contributor' NOT NULL,
	`suspended` integer DEFAULT 0 NOT NULL,
	`created` integer NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `profiles_handle_unique` ON `profiles` (`handle`);--> statement-breakpoint
CREATE TABLE `slots` (
	`mission` text PRIMARY KEY NOT NULL,
	`user` text,
	`handle` text,
	`expires` integer DEFAULT 0 NOT NULL,
	`state` text DEFAULT 'available' NOT NULL,
	`note` text DEFAULT '' NOT NULL,
	`version` integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE `submissions` (
	`id` text PRIMARY KEY NOT NULL,
	`mission` text NOT NULL,
	`user` text NOT NULL,
	`handle` text NOT NULL,
	`body` text NOT NULL,
	`created` integer NOT NULL,
	`status` text DEFAULT 'submitted' NOT NULL,
	`note` text DEFAULT '' NOT NULL,
	`commit` text
);
--> statement-breakpoint
CREATE INDEX `submissions_user_created` ON `submissions` (`user`,`created`);