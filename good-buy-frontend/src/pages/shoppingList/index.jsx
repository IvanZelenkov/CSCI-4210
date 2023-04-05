import { motion } from "framer-motion";
import * as React from 'react';
// import React, { Component } from 'react';
import Checkbox from '@mui/material/Checkbox';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

const label = { inputProps: { 'aria-label': 'Checkbox demo' } };
const name = "ShoppingList";
const itemCount = 2;
const shopCount = 2;



const ShoppingList = () => {

	const generateGrid = () => {
		return(
				<Grid container spacing={5}
					justifyContent = "center"
					display = "flex"
					alignItems = "stretch"
					direction = "row">
				  <Grid item xs={1}>
					  <div>
						<Checkbox {...label} defaultChecked />
						<Checkbox {...label} />
						<Checkbox {...label} disabled />
						<Checkbox {...label} disabled checked />
					</div>
			
					  </Grid>
					  <Grid item xs={4.5}>
						<Box style = {{color: "black"}}>itemname</Box>
					  </Grid>
					  <Grid item xs ={1}>
						  <div>
							<Checkbox {...label} defaultChecked />
							<Checkbox {...label} />
							<Checkbox {...label} disabled />
							<Checkbox {...label} disabled checked />
						</div>
					  </Grid>
					<Grid item xs ={4.5}>
						<Box style = {{color: "black"}}>itemname</Box>
					</Grid>
				</Grid>
			
			);


	}

	return (
		<div
			className = "List-Container"
			>
				
			<h2 style = {{color:"black", textAlign: "center", fontSize: 50}}>{name}</h2>	

			{generateGrid()}

		</div>



	);
}



export default ShoppingList;