import { z } from 'zod';

export const formSchema = z.object({
	appName: z.string().min(2).max(50),
	storeId: z.string().min(2).max(50),
	appStore: z.enum(['ios', 'android'], {
		required_error: 'You need to select an app store.'
	})
});

export type FormSchema = typeof formSchema;
