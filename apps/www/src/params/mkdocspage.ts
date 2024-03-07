import type { ParamMatcher } from '@sveltejs/kit';

export const match: ParamMatcher = (param) => {
	// Any string that does not have a . in it
	// return !/\./.test(param);
	return !param.includes('.');
};
