<script lang="ts">
	import File from 'lucide-svelte/icons/file';
	// import Home from "lucide-svelte/icons/home";
	import LineChart from 'lucide-svelte/icons/chart-column';
	import ListFilter from 'lucide-svelte/icons/list-filter';
	import Ellipsis from 'lucide-svelte/icons/ellipsis';
	import Package from 'lucide-svelte/icons/package';
	import Package2 from 'lucide-svelte/icons/package-2';
	import PanelLeft from 'lucide-svelte/icons/panel-left';
	import CirclePlus from 'lucide-svelte/icons/circle-plus';
	import Search from 'lucide-svelte/icons/search';
	import Settings from 'lucide-svelte/icons/settings';
	import ShoppingCart from 'lucide-svelte/icons/shopping-cart';
	import UsersRound from 'lucide-svelte/icons/users-round';

	import { Badge } from '$lib/components/ui/badge/index';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index';
	import { Button } from '$lib/components/ui/button/index';
	import * as Card from '$lib/components/ui/card/index';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index';
	import { Input } from '$lib/components/ui/input/index';
	import * as Sheet from '$lib/components/ui/sheet/index';
	import * as Table from '$lib/components/ui/table/index';
	import * as Tabs from '$lib/components/ui/tabs/index';
	import * as Tooltip from '$lib/components/ui/tooltip/index';
</script>

<div class="bg-muted/40 flex min-h-screen w-full flex-col">
	<div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
		<header
			class="bg-background sticky top-0 z-30 flex h-14 items-center gap-4 border-b px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6"
		>
			<Sheet.Root>
				<Sheet.Trigger asChild let:builder>
					<Button builders={[builder]} size="icon" variant="outline" class="sm:hidden">
						<PanelLeft class="h-5 w-5" />
						<span class="sr-only">Toggle Menu</span>
					</Button>
				</Sheet.Trigger>
			</Sheet.Root>
			<Breadcrumb.Root class="hidden md:flex">
				<Breadcrumb.List>
					<Breadcrumb.Item>
						<Breadcrumb.Link href="/integrations">Integrations</Breadcrumb.Link>
					</Breadcrumb.Item>
					<Breadcrumb.Separator />
					<Breadcrumb.Item>
						<Breadcrumb.Link href="/integrations/networks">Networks</Breadcrumb.Link>
					</Breadcrumb.Item>
				</Breadcrumb.List>
			</Breadcrumb.Root>
		</header>
		<main class="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8">
			<Tabs.Root value="all">
				<div class="flex items-center">
					<Tabs.List>
						<Tabs.Trigger value="all">All</Tabs.Trigger>
						<Tabs.Trigger value="active">Active</Tabs.Trigger>
						<Tabs.Trigger value="draft">Draft</Tabs.Trigger>
						<Tabs.Trigger value="archived" class="hidden sm:flex">Archived</Tabs.Trigger>
					</Tabs.List>
					<div class="ml-auto flex items-center gap-2">
						<DropdownMenu.Root>
							<DropdownMenu.Trigger asChild let:builder>
								<Button builders={[builder]} variant="outline" size="sm" class="h-8 gap-1">
									<ListFilter class="h-3.5 w-3.5" />
									<span class="sr-only sm:not-sr-only sm:whitespace-nowrap"> Filter </span>
								</Button>
							</DropdownMenu.Trigger>
							<DropdownMenu.Content align="end">
								<DropdownMenu.Label>Filter by</DropdownMenu.Label>
								<DropdownMenu.Separator />
								<DropdownMenu.CheckboxItem checked>Active</DropdownMenu.CheckboxItem>
								<DropdownMenu.CheckboxItem>Draft</DropdownMenu.CheckboxItem>
								<DropdownMenu.CheckboxItem>Archived</DropdownMenu.CheckboxItem>
							</DropdownMenu.Content>
						</DropdownMenu.Root>
					</div>
				</div>
				<Tabs.Content value="all">
					<Card.Root>
						<Card.Header>
							<Card.Title>Networks</Card.Title>
							<Card.Description>Manage your ad network integrations.</Card.Description>
						</Card.Header>
						<Card.Content>
							<Table.Root>
								<Table.Header>
									<Table.Row>
										<Table.Head class="hidden w-[100px] sm:table-cell">
											<span class="sr-only">Image</span>
										</Table.Head>
										<Table.Head>Name</Table.Head>
										<Table.Head>Status</Table.Head>
										<Table.Head class="hidden md:table-cell">Price</Table.Head>
										<Table.Head class="hidden md:table-cell">Total Sales</Table.Head>
										<Table.Head class="hidden md:table-cell">Created at</Table.Head>
										<Table.Head>
											<span class="sr-only">Actions</span>
										</Table.Head>
									</Table.Row>
								</Table.Header>
								<Table.Body>
									<Table.Row>
										<Table.Cell class="hidden sm:table-cell">
											<img
												alt="Product example"
												class="aspect-square rounded-md object-cover"
												height="64"
												src="/images/placeholder.svg"
												width="64"
											/>
										</Table.Cell>
										<Table.Cell class="font-medium">Laser Lemonade Machine</Table.Cell>
										<Table.Cell>
											<Badge variant="outline">Draft</Badge>
										</Table.Cell>
										<Table.Cell class="hidden md:table-cell">$499.99</Table.Cell>
										<Table.Cell class="hidden md:table-cell">25</Table.Cell>
										<Table.Cell class="hidden md:table-cell">2023-07-12 10:42 AM</Table.Cell>
										<Table.Cell>
											<DropdownMenu.Root>
												<DropdownMenu.Trigger asChild let:builder>
													<Button
														aria-haspopup="true"
														size="icon"
														variant="ghost"
														builders={[builder]}
													>
														<Ellipsis class="h-4 w-4" />
														<span class="sr-only">Toggle menu</span>
													</Button>
												</DropdownMenu.Trigger>
												<DropdownMenu.Content align="end">
													<DropdownMenu.Label>Actions</DropdownMenu.Label>
													<DropdownMenu.Item>Edit</DropdownMenu.Item>
													<DropdownMenu.Item>Delete</DropdownMenu.Item>
												</DropdownMenu.Content>
											</DropdownMenu.Root>
										</Table.Cell>
									</Table.Row>
									<Table.Row>
										<Table.Cell class="hidden sm:table-cell">
											<img
												alt="Product"
												class="aspect-square rounded-md object-cover"
												height="64"
												src="/images/placeholder.svg"
												width="64"
											/>
										</Table.Cell>
										<Table.Cell class="font-medium">Hypernova Headphones</Table.Cell>
										<Table.Cell>
											<Badge variant="outline">Active</Badge>
										</Table.Cell>
										<Table.Cell class="hidden md:table-cell">$129.99</Table.Cell>
										<Table.Cell class="hidden md:table-cell">100</Table.Cell>
										<Table.Cell class="hidden md:table-cell">2023-10-18 03:21 PM</Table.Cell>
										<Table.Cell>
											<DropdownMenu.Root>
												<DropdownMenu.Trigger asChild let:builder>
													<Button
														builders={[builder]}
														aria-haspopup="true"
														size="icon"
														variant="ghost"
													>
														<Ellipsis class="h-4 w-4" />
														<span class="sr-only">Toggle menu</span>
													</Button>
												</DropdownMenu.Trigger>
												<DropdownMenu.Content align="end">
													<DropdownMenu.Label>Actions</DropdownMenu.Label>
													<DropdownMenu.Item>Edit</DropdownMenu.Item>
													<DropdownMenu.Item>Delete</DropdownMenu.Item>
												</DropdownMenu.Content>
											</DropdownMenu.Root>
										</Table.Cell>
									</Table.Row>
								</Table.Body>
							</Table.Root>
						</Card.Content>
						<Card.Footer></Card.Footer>
					</Card.Root>
				</Tabs.Content>
			</Tabs.Root>
		</main>
	</div>
</div>
