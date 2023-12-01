import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const oaTheme: CustomThemeConfig = {
	name: 'oa-theme',
	properties: {
		// =~= Theme Properties =~=
		'--theme-font-family-base': `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		'--theme-font-family-heading': `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		'--theme-font-color-base': '0 0 0',
		'--theme-font-color-dark': '255 255 255',
		'--theme-rounded-base': '4px',
		'--theme-rounded-container': '0px',
		'--theme-border-base': '1px',
		// =~= Theme On-X Colors =~=
		'--on-primary': '255 255 255',
		'--on-secondary': '0 0 0',
		'--on-tertiary': '0 0 0',
		'--on-success': '0 0 0',
		'--on-warning': '0 0 0',
		'--on-error': '0 0 0',
		'--on-surface': '255 255 255',
		// =~= Theme Colors  =~=
		// primary | #3d3846
		'--color-primary-50': '226 225 227', // #e2e1e3
		'--color-primary-100': '216 215 218', // #d8d7da
		'--color-primary-200': '207 205 209', // #cfcdd1
		'--color-primary-300': '177 175 181', // #b1afb5
		'--color-primary-400': '119 116 126', // #77747e
		'--color-primary-500': '61 56 70', // #3d3846
		'--color-primary-600': '55 50 63', // #37323f
		'--color-primary-700': '46 42 53', // #2e2a35
		'--color-primary-800': '37 34 42', // #25222a
		'--color-primary-900': '30 27 34', // #1e1b22
		// secondary | #f6dd39
		'--color-secondary-50': '254 250 225', // #fefae1
		'--color-secondary-100': '253 248 215', // #fdf8d7
		'--color-secondary-200': '253 247 206', // #fdf7ce
		'--color-secondary-300': '251 241 176', // #fbf1b0
		'--color-secondary-400': '249 231 116', // #f9e774
		'--color-secondary-500': '246 221 57', // #f6dd39
		'--color-secondary-600': '221 199 51', // #ddc733
		'--color-secondary-700': '185 166 43', // #b9a62b
		'--color-secondary-800': '148 133 34', // #948522
		'--color-secondary-900': '121 108 28', // #796c1c
		// tertiary | #acfa87
		'--color-tertiary-50': '243 254 237', // #f3feed
		'--color-tertiary-100': '238 254 231', // #eefee7
		'--color-tertiary-200': '234 254 225', // #eafee1
		'--color-tertiary-300': '222 253 207', // #defdcf
		'--color-tertiary-400': '197 252 171', // #c5fcab
		'--color-tertiary-500': '172 250 135', // #acfa87
		'--color-tertiary-600': '155 225 122', // #9be17a
		'--color-tertiary-700': '129 188 101', // #81bc65
		'--color-tertiary-800': '103 150 81', // #679651
		'--color-tertiary-900': '84 123 66', // #547b42
		// success | #a055f3
		'--color-success-50': '241 230 253', // #f1e6fd
		'--color-success-100': '236 221 253', // #ecddfd
		'--color-success-200': '231 213 252', // #e7d5fc
		'--color-success-300': '217 187 250', // #d9bbfa
		'--color-success-400': '189 136 247', // #bd88f7
		'--color-success-500': '160 85 243', // #a055f3
		'--color-success-600': '144 77 219', // #904ddb
		'--color-success-700': '120 64 182', // #7840b6
		'--color-success-800': '96 51 146', // #603392
		'--color-success-900': '78 42 119', // #4e2a77
		// warning | #e6a5f8
		'--color-warning-50': '251 242 254', // #fbf2fe
		'--color-warning-100': '250 237 254', // #faedfe
		'--color-warning-200': '249 233 253', // #f9e9fd
		'--color-warning-300': '245 219 252', // #f5dbfc
		'--color-warning-400': '238 192 250', // #eec0fa
		'--color-warning-500': '230 165 248', // #e6a5f8
		'--color-warning-600': '207 149 223', // #cf95df
		'--color-warning-700': '173 124 186', // #ad7cba
		'--color-warning-800': '138 99 149', // #8a6395
		'--color-warning-900': '113 81 122', // #71517a
		// error | #5c997c
		'--color-error-50': '231 240 235', // #e7f0eb
		'--color-error-100': '222 235 229', // #deebe5
		'--color-error-200': '214 230 222', // #d6e6de
		'--color-error-300': '190 214 203', // #bed6cb
		'--color-error-400': '141 184 163', // #8db8a3
		'--color-error-500': '92 153 124', // #5c997c
		'--color-error-600': '83 138 112', // #538a70
		'--color-error-700': '69 115 93', // #45735d
		'--color-error-800': '55 92 74', // #375c4a
		'--color-error-900': '45 75 61', // #2d4b3d
		// surface | #241f31
		'--color-surface-50': '222 221 224', // #dedde0
		'--color-surface-100': '211 210 214', // #d3d2d6
		'--color-surface-200': '200 199 204', // #c8c7cc
		'--color-surface-300': '167 165 173', // #a7a5ad
		'--color-surface-400': '102 98 111', // #66626f
		'--color-surface-500': '36 31 49', // #241f31
		'--color-surface-600': '32 28 44', // #201c2c
		'--color-surface-700': '27 23 37', // #1b1725
		'--color-surface-800': '22 19 29', // #16131d
		'--color-surface-900': '18 15 24' // #120f18
	}
};
