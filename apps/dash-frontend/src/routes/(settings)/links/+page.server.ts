import type { PageServerLoad, Actions } from './$types';

import { superValidate, message } from 'sveltekit-superforms';

import { domainSchema } from '$schemas';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
	createClientDomain: async (event) => {
		console.log('createClientDomain');
		const form = await superValidate(event, zod(domainSchema));

		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const domain = form.data.clientDomain;

		console.log(`Actions: Client Domain: ${domain}`);

		const response = await fetch(`http://dash-backend:8001/api/links/domains/${domain}`, {
			method: 'POST'
		});

		if (!response.ok) {
			const resText = await response.text();

			if (resText.includes('already exists')) {
				return message(form, 'This domain already exists.', {
					status: 400
				});
			}

			const truncatedText = resText.substring(0, 100);
			console.log(`Server failed to save the domain (${response.status}): ${truncatedText}`);
			return message(form, `backend error:	 (${response.status}): ${truncatedText}`, {
				status: 500
			});
		}

		return message(form, 'success');
	},
	deleteClientDomain: async ({ request }) => {
		const data = await request.formData();
		const id = data.get('id');

		console.log(`Domain id: ${id}`);

		const response = await fetch(`http://dash-backend:8001/api/links/domains/${id}`, {
			method: 'DELETE'
		});

		// Check if the request was successful
		if (!response.ok) {
			console.error('Failed to delete the domain');
			// Optionally, you could return some error state or message here
			return { error: 'Failed to delete the domain' };
		}
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ parent }) => {
	const { clientDomains } = await parent();

	return {
		linksData: fetch(`http://dash-backend:8001/api/links`)
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
		clientDomains,
		form: await superValidate(zod(domainSchema))
	};
};
