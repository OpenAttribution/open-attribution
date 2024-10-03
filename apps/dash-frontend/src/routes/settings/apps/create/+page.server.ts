import type { Actions, PageServerLoad } from './$types.js';
import { superValidate } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';

import { fail } from '@sveltejs/kit';

export const actions = {
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
		form: await superValidate(zod(formSchema))
	};
};
