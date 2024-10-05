import type { Actions, PageServerLoad } from './$types.js';
import { superValidate, message } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
	createApp: async (event) => {
		const form = await superValidate(event, zod(formSchema));

		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const store_id = form.data.storeId;
		const app_name = form.data.appName;
		const app_store = form.data.appStore;

		console.log(`Create app Name: ${app_name}, ${app_store}, ${store_id}`);

		const response = await fetch(
			`http://dash-backend:8001/api/apps/${store_id}?app_name=${app_name}&store=${app_store}`,
			{
				method: 'POST'
			}
		);

		if (!response.ok) {
			return message(
				form,
				`Server failed to save the app (${response.status}): ${(await response.text()) || 'Unknown error'}`,
				{ status: 500 }
			);
		}

		return {
			form
		};
	}
} satisfies Actions;

export const load: PageServerLoad = async ({}) => {
	return {
		form: await superValidate(zod(formSchema))
	};
};
