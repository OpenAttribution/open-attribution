<script lang="ts">
	import CircleUser from 'lucide-svelte/icons/circle-user';
	import Menu from 'lucide-svelte/icons/menu';
	import Package2 from 'lucide-svelte/icons/package-2';
	import Search from 'lucide-svelte/icons/search';

	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import { Checkbox } from '$lib/components/ui/checkbox/index';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index';
	import { Input } from '$lib/components/ui/input/index';
	import * as Sheet from '$lib/components/ui/sheet/index';
</script>

<div class="flex min-h-screen w-full flex-col">
	<main
		class="bg-muted/40 flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 p-4 md:gap-8 md:p-10"
	>
		<div class="mx-auto grid w-full max-w-6xl gap-2">
			<h1 class="text-3xl font-semibold">Support</h1>
		</div>
		<div class="mx-auto grid w-full max-w-6xl items-start gap-6">
			<div class="grid gap-6">
				<Card.Root>
					<Card.Header>
						<Card.Title>Documentation</Card.Title>
					</Card.Header>
					<Card.Content>
						The documentation on <a
							class="text-muted-foreground hover:text-primary transition-colors"
							href="https://openattribution.dev/docs">OpenAttribution.dev/docs</a
						> is the best way to get yourself started.
					</Card.Content>
				</Card.Root>

				<Card.Root>
					<Card.Header>
						<Card.Title>Discord</Card.Title>
					</Card.Header>
					<Card.Content>
						Discord is a gathering place for the community. A quick way to ask high level questions
						or hear from others. <a
							class="text-muted-foreground hover:text-primary transition-colors"
							href="https://discord.gg/Z5ueYE3Ct3">Join here.</a
						>
					</Card.Content>
				</Card.Root>

				<Card.Root>
					<Card.Header>
						<Card.Title>GitHub Issues & Discussions</Card.Title>
					</Card.Header>
					<Card.Content>
						Contributing to OpenAttribution's <a
							class="text-muted-foreground hover:text-primary transition-colors"
							href="https://github.com/OpenAttribution/open-attribution/issues"
							>GitHub public issues and discussions</a
						> is probably the best way to get in contact with others.
					</Card.Content>
				</Card.Root>
			</div>
		</div>
	</main>
</div>
