import { z } from 'zod';

export const formSchema = z.object({
	appName: z.string().min(2).max(50),
	storeId: z.string().min(2).max(50),
	appStore: z.string().min(2).max(50)
});

export type FormSchema = typeof formSchema;
