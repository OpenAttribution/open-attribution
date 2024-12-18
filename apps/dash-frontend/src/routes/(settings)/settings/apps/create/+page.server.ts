import type { Actions, PageServerLoad } from './$types.js';
import { redirect } from '@sveltejs/kit';
import { superValidate, message } from 'sveltekit-superforms';
import { appSchema } from '$schemas';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
	createApp: async (event) => {
		const form = await superValidate(event, zod(appSchema));

		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const store_id = form.data.storeId;
		const app_name = form.data.appName;
		const app_store = form.data.appStore;
		const apple_team_id = form.data.appleTeamId;
		const bundle_id = form.data.bundleId;
		const google_sha256_fingerprints = form.data.googleSha256Fingerprints;

		console.log(`Create app Name: ${app_name}, ${app_store}, ${store_id}`);

		const response = await fetch(`http://dash-backend:8001/api/apps/${store_id}`, {
			method: 'POST',
			body: JSON.stringify({
				app_name: app_name,
				store: app_store,
				apple_team_id: apple_team_id,
				bundle_id: bundle_id,
				google_sha256_fingerprints: Array.isArray(google_sha256_fingerprints)
					? google_sha256_fingerprints
					: [google_sha256_fingerprints]
			})
		});

		if (!response.ok) {
			return message(
				form,
				`Server failed to save the app (${response.status}): ${(await response.text()) || 'Unknown error'}`,
				{ status: 500 }
			);
		}

		throw redirect(302, '/settings/apps');
	}
} satisfies Actions;

export const load: PageServerLoad = async ({}) => {
	return {
		form: await superValidate(zod(appSchema))
	};
};
