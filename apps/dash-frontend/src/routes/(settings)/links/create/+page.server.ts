import type { Actions, PageServerLoad } from './$types.js';
import { redirect } from '@sveltejs/kit';
import { superValidate, message } from 'sveltekit-superforms';
import { linkSchema } from '$schemas';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
	createLink: async (event) => {
		const form = await superValidate(event, zod(linkSchema));

		console.log(`Form is valid: ${form.valid}`);

		if (!form.valid) {
			console.log(`Form is not valid: ${JSON.stringify(form.data)}`);
			return fail(400, {
				form
			});
		}

		const android_app_id = form.data.googleAppId;
		const ios_app_id = form.data.appleAppId;
		const domain_id = form.data.domainId;
		const share_slug = form.data.shareSlug;
		const network_id = form.data.networkId;
		const campaign_name = form.data.campaignName;
		const ad_name = form.data.adName;

		const apiUrl = `links/${domain_id}?google_app_id=${android_app_id}&apple_app_id=${ios_app_id}&share_slug=${share_slug}&network_id=${network_id}&campaign_name=${campaign_name}&ad_name=${ad_name}`;

		console.log(`Create share link ${apiUrl}`);

		const response = await fetch(`http://dash-backend:8001/api/${apiUrl}`, {
			method: 'POST'
		});

		if (!response.ok) {
			return message(
				form,
				`Server failed to save the app (${response.status}): ${(await response.text()) || 'Unknown error'}`,
				{ status: 500 }
			);
		}

		throw redirect(302, `/links`);
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ parent }) => {
	const { respApps, respNets, clientDomains } = await parent();

	return {
		respApps: respApps,
		respNets: respNets,
		clientDomains: clientDomains,
		form: await superValidate(zod(linkSchema))
	};
};
