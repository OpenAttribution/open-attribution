import type { Actions, PageServerLoad } from './$types';

import { superValidate, message } from 'sveltekit-superforms';

import { networkSchema } from '$schemas';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
	createCustomIntegration: async (event) => {
		console.log('createCustomIntegration');
		const form = await superValidate(event, zod(networkSchema));

		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const name = form.data.networkName;
		const postback_id = form.data.postbackId;

		console.log(`Actions: Network Name: ${name} Postback ID: ${postback_id}`);

		const response = await fetch(
			`http://dash-backend:8001/api/networks/${postback_id}?network_name=${name}`,
			{
				method: 'POST'
			}
		);

		if (!response.ok) {
			const resText = await response.text();

			if (resText.includes('already exists')) {
				return message(form, 'This name or postback ID already exists.', {
					status: 400
				});
			}

			const truncatedText = resText.substring(0, 100);
			console.log(`Server failed to save the network (${response.status}): ${truncatedText}`);
			return message(form, `backend error:	 (${response.status}): ${truncatedText}`, {
				status: 500
			});
		}

		return message(form, 'success');
	},

	deleteIntegration: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		console.log(`Network id: ${id}`);

		const response = await fetch(`http://dash-backend:8001/api/networks/${id}`, {
			method: 'DELETE'
		});

		// Check if the request was successful
		if (!response.ok) {
			console.error('Failed to delete the network');
			// Optionally, you could return some error state or message here
			return { error: 'Failed to delete the network' };
		}
	}
} satisfies Actions;

export const load: PageServerLoad = async ({}) => {
	return {
		respData: fetch(`http://dash-backend:8001/api/networks`)
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
			),
		form: await superValidate(zod(networkSchema))
	};
};
