import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';


export class OffersTable extends React.Component{
    state = {
        offers: [
            {
                id: 1,
                titre: "donnée de test 1",
                ville: "Luxembourg",
                prix: 300000,
                prix_m2: 8700.4,
                annonce: "https://www.athome.lu/vente/bureau/luxembourg/id-6341686.html"
            },
            {
                id: 2,
                titre: "donnée de test 2",
                ville: "Bruges",
                prix: 400000,
                prix_m2: 5900.4,
                annonce: "https://www.athome.lu/vente/bureau/luxembourg/id-6341686.html"
            },
            {
                id: 3,
                titre: "donnée de test 3",
                ville: "Faro",
                prix: 467000,
                prix_m2: 9800.6943523,
                annonce: "https://www.athome.lu/vente/bureau/luxembourg/id-6341686.html"
            },
            {
                id: 4,
                titre: "donnée de test 4",
                ville: "Cabeça de cabra",
                prix: 670000,
                prix_m2: 5900.43,
                annonce: "https://www.athome.lu/vente/bureau/luxembourg/id-6341686.html"
            }
        ] 
    }

	render() {
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
                        <TableRow key={row.id}>
                        <TableCell component="th" scope="row">
                            {row.id}
                        </TableCell>
                        <TableCell align="right">{row.titre}</TableCell>
                        <TableCell align="right">{row.ville}</TableCell>
                        <TableCell align="right">{row.prix}</TableCell>
                        <TableCell align="right">{parseFloat(row.prix_m2).toFixed(2)}</TableCell>
                        <TableCell align="right"><a href={row.annonce} target="_blank">Annonce </a></TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
			</div>
		)
	}
}