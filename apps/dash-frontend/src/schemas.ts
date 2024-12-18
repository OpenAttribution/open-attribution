import { z } from 'zod';

export const linkSchema = z.object({
	googleAppId: z.number().optional().nullable().default(null),
	// googleAppName: z.string(), // Used for display
	appleAppId: z.number().optional().nullable().default(null),
	// appleAppName: z.string(), // Used for display
	domainId: z.number(),
	shareSlug: z
		.string()
		.min(1)
		.max(50)
		.regex(/^[a-zA-Z0-9-_]+$/, {
			message: 'Share slug can only contain alphanumeric characters, dashes, and underscores.'
		}),
	webLandingPage: z.string().min(2).max(50),
	networkId: z.number(),
	// networkName: z.string(), // Used for display
	campaignName: z.string().min(2).max(100),
	adName: z.string().max(50).optional().default('')
});
export type LinkSchema = typeof linkSchema;

export const appSchema = z.object({
	appName: z.string().min(2).max(50),
	storeId: z.string().min(2).max(50),
	bundleId: z.string().min(2).max(100).optional().nullable().default(null),
	appleTeamId: z.string().min(2).max(25).optional().nullable().default(null),
	googleSha256Fingerprints: z
		.string()
		.min(64)
		.max(98)
		.regex(/^[a-fA-F0-9.:-]+$/, {
			message: 'Google SHA256 Fingerprints must be a valid SHA256 hash.'
		})
		.optional()
		.nullable()
		.default(null),
	appStore: z.enum(['ios', 'android'], {
		required_error: 'You need to select an app store.'
	})
});
export type AppSchema = typeof appSchema;

export const networkSchema = z.object({
	networkName: z.string().min(2).max(50),
	postbackId: z
		.string()
		.min(2, { message: 'Postback ID must be at least 2 characters long.' })
		.max(50, { message: 'Postback ID must not exceed 50 characters.' })
		.regex(/^[a-zA-Z0-9-_]+$/, {
			message: 'Postback ID can only contain alphanumeric characters, dashes, and underscores.'
		})
});
export type NetworkSchema = typeof networkSchema;

export const domainSchema = z.object({
	clientDomain: z
		.string()
		.min(2)
		.max(50)
		.regex(/^[a-zA-Z0-9.-]+$/, {
			message: 'Domain must be a valid top level domain or subdomain without special characters.'
		})
});
export type DomainSchema = typeof domainSchema;
