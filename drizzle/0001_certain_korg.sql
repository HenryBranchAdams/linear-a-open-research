CREATE TABLE `contribution_records` (
	`id` text PRIMARY KEY NOT NULL,
	`post_id` text NOT NULL,
	`title` text NOT NULL,
	`target` text DEFAULT '' NOT NULL,
	`sources` text DEFAULT '' NOT NULL,
	`method` text DEFAULT '' NOT NULL,
	`uncertainty` text DEFAULT 'Not stated' NOT NULL,
	`exposure` text DEFAULT 'Not declared' NOT NULL,
	`credit` text DEFAULT '' NOT NULL,
	`license` text DEFAULT 'UNSPECIFIED' NOT NULL,
	`related_id` text,
	FOREIGN KEY (`id`) REFERENCES `submissions`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `contribution_records_post_id_unique` ON `contribution_records` (`post_id`);--> statement-breakpoint
CREATE INDEX `contribution_records_related` ON `contribution_records` (`related_id`);