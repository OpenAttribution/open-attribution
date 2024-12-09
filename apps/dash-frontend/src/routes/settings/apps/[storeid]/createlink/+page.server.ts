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

		const app_id = form.data.appId;
		const store_id = form.data.storeId;
		const share_id = form.data.shareId;
		const network_id = form.data.networkId;
		const campaign_name = form.data.campaignName;
		const ad_name = form.data.adName;

		console.log(
			`Create share link app:${app_id}, share:${share_id}, network:${network_id}, campaign:${campaign_name}, ad:${ad_name}`
		);

		const response = await fetch(
			`http://dash-backend:8001/api/apps/${app_id}/links?share_id=${share_id}&network_id=${network_id}&campaign_name=${campaign_name}&ad_name=${ad_name}`,
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

		throw redirect(302, `/settings/apps/${store_id}`);
	}
} satisfies Actions;

export const load: PageServerLoad = async ({ parent }) => {
	const { appData } = await parent();

	return {
		appData: appData,
		form: await superValidate(zod(linkSchema))
	};
};
