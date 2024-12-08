import { z } from 'zod';

export const linkSchema = z.object({
	appId: z.number(),
	storeId: z.string(),
	shareId: z.string().min(2).max(50),
	network: z.string().min(2).max(50),
	campaignName: z.string().min(2).max(50),
	adName: z.string().min(2).max(50).optional()
});
export type LinkSchema = typeof linkSchema;

export const appSchema = z.object({
	appName: z.string().min(2).max(50),
	storeId: z.string().min(2).max(50),
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
