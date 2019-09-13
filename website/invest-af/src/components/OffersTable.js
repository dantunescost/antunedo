import React from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import axios from 'axios';


export class OffersTable extends React.Component{
    constructor(props){
        super(props);
        this.state = {offers: []};
        this.getOffers = this.getOffers.bind(this);
    }

    getOffers() {
        var self = this;
        axios.get('http://127.0.0.1:8080/getOffers', {headers: {"Access-Control-Allow-Origin": "*"}})
            .then(function (response) {
                self.setState({offers: response.data});
            }).catch(function (error) {
                if (error.response) {
                  console.log(error.response.headers);
                } 
                else if (error.request) {
                  console.log(error.request);
                } 
                else {
                  console.log(error);
                  console.log(error.message);
                }
                console.log(error.config);
            });
    }

	render() {
        this.getOffers();
		return (
			<div style={{width: "70%", margin: "0 auto"}}>
                <Table >
                    <TableHead>
                    <TableRow>
                        <TableCell>ID</TableCell>
                        <TableCell align="right">Titre</TableCell>
                        <TableCell align="right">Ville</TableCell>
                        <TableCell align="right">Prix (€)</TableCell>
                        <TableCell align="right">Prix au m² (€/m²)</TableCell>
                        <TableCell align="right">Annonce</TableCell>                       
                    </TableRow>
                    </TableHead>
                    <TableBody>
                    {this.state.offers.map(row => (
                        <TableRow key={this.state.offers.indexOf(row)}>
                            <TableCell component="th" scope="row">{row.id}</TableCell>
                            <TableCell align="right">{row.title}</TableCell>
                            <TableCell align="right">{row.city}</TableCell>
                            <TableCell align="right">{row.price}</TableCell>
                            <TableCell align="right">{parseFloat(row.price_per_m2).toFixed(2)}</TableCell>
                            <TableCell align="right"><a href={row.url} target="_blank" rel="noopener noreferrer">Annonce </a></TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
			</div>
		)
	}
}