<template>
  <header>
		<router-link to="/" class="nav-link" exact><h1>NYT Crossword Stats</h1></router-link>
		<nav>
			<router-link to="/leaderboard" class="nav-link" exact>Head-To-Head</router-link>
			<router-link to="/leaderboard-averages" class="nav-link" exact>Mini Averages</router-link>
		</nav>
  </header>
</template>

<style scoped lang="scss">
	header {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 16px 24px;
		border: 1px solid $PRIMARY_100;
		border-radius: 0 0 8px 8px;
		box-shadow: 0px 4px 10px -4px rgba(0, 30, 43, 0.3);

		a {
			text-decoration: none;
			color: inherit;
		}

		h1 {
			text-align: center;
			font-size: 24px;
		}

		nav {
			display: flex;
			flex-direction: column;
			margin-top: 8px;

			a {
				font-size: 14px;
				text-transform: uppercase;
				text-decoration: none;
				color: $PRIMARY_800;
				margin: 2px 0;
				padding: 8px 10px;
				border-radius: 4px;
				transition: ease-in-out 0.3s;

				&:hover {
					background-color: $PRIMARY_300;
				}

				&.active {
					background-color: $PRIMARY_500;
					color: $WHITE;
				}
			}
		}

		@media (min-width: $BREAKPOINT_SM) {
			nav {
				flex-direction: row;

				a {
					margin: 0 12px 0 0;

					&:last-of-type {
						margin-right: 0;
					}
				}
			}
		}

		@media (min-width: $BREAKPOINT_MD) {
			padding: 24px 32px;
			flex-direction: row;
			justify-content: space-between;

			h1 {
				font-size: 32px;
			}

			nav {
				a {
					font-size: 16px;
				}
			}
		}
	}
</style>