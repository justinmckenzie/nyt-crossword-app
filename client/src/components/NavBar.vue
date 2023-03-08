<template>
  <header>
		<h1>NYT Crossword Stats</h1>
		<nav>
			<router-link to="/" class="nav-link" exact>Home</router-link>
			<router-link to="/leaderboard" class="nav-link" exact>Head-To-Head</router-link>
			<router-link to="/leaderboard-averages" class="nav-link" exact>Mini Averages</router-link>
		</nav>
  </header>
</template>

<style scoped lang="scss">
	header {
		position: fixed;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 24px 32px;
		top: 0;
		width: 100%;
		border-radius: 0 0 8px 8px;
		border: 1px solid $PRIMARY_100;
    box-shadow: 0px 4px 10px -4px rgba(0, 30, 43, 0.3);
	}

	nav {
		a {
			text-transform: uppercase;
			text-decoration: none;
			color: $PRIMARY_800;
			padding: 8px 10px;
			margin-right: 12px;
			border-radius: 4px;
			transition: ease-in-out 0.3s;

			&:hover {
				background-color: $PRIMARY_500;
				color: $WHITE;
			}

			&:last-of-type {
				margin-right: 0;
			}
		}
	}
</style>