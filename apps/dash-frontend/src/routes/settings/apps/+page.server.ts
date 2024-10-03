import type { Actions, PageServerLoad } from './$types.js';
import { superValidate } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
	createApp: async ({ request }) => {
		const data = await request.formData();
		const store_id = data.get('store_id');
		const app_name = data.get('app_name');
		const store = data.get('store');

		console.log(`Create app Name: ${app_name}`);

		const response = await fetch(
			`http://dash-backend:8001/api/apps/${store_id}?app_name=${app_name}&store=${store}`,
			{
				method: 'POST'
			}
		);

		// Check if the request was successful
		if (!response.ok) {
			console.error('Failed to add the app');
			return { error: 'Failed to add the app' };
		}
	},

	deleteApp: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		console.log(`Delete app id: ${id}`);

		const response = await fetch(`http://dash-backend:8001/api/networks/${id}`, {
			method: 'DELETE'
		});

		// Check if the request was successful
		if (!response.ok) {
			console.error('Failed to delete the network');
			// Optionally, you could return some error state or message here
			return { error: 'Failed to delete the network' };
		}
	},

	newAppCreate: async (event) => {
		const form = await superValidate(event, zod(formSchema));

		if (!form.valid) {
			return fail(400, {
				form
			});
		}
		return {
			form
		};
	}
} satisfies Actions;

export const load: PageServerLoad = async ({}) => {
	return {
		form: await superValidate(zod(formSchema)),
		respData: fetch(`http://dash-backend:8001/api/apps`)
			.then((resp) => {
				if (resp.status === 200) {
					return resp.json();
				} else if (resp.status === 404) {
					console.log('Not found');
					return 'Not Found';
				} else if (resp.status === 500) {
					console.log('API Server error');
					return 'Backend Error';
				}
			})
			.then(
				(json) => json,
				(error) => {
					console.log('Uncaught error', error);
					return 'Uncaught Error';
				}
			)
	};
};
