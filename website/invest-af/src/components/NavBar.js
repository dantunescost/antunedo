import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

export class NavBar extends React.Component{
	render() {
		return (
			<div>
				<AppBar position="static">
					<Toolbar>
						<Typography variant="title" color="inherit">
							Invest projet
						</Typography>
					</Toolbar>
				</AppBar>
			</div>
		)
	}
}