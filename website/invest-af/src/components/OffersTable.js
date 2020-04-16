import React, {useState, useEffect} from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import RoomIcon from '@material-ui/icons/Room';
import HomeTwoToneIcon from '@material-ui/icons/HomeTwoTone';
import Tooltip from '@material-ui/core/Tooltip';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import GeoEntryField from './GeoEntryField';
import Grid from '@material-ui/core/Grid';
import PriceSlider from './PriceSlider';
import SurfaceSlider from './SurfaceSlider';
import TerrainSlider from './TerrainSlider';
import PricePerM2Slider from './PricePerM2Slider';
import PricePerAreSlider from './PricePerAreSlider';
import MagicRatioSlider from './MagicRatioSlider';
import Paper from "@material-ui/core/Paper";
import TablePaginationActions from './TablePaginationActions';
import axios from 'axios';
import PropertyTypeField from './PropertyTypeField';


const useStyles = makeStyles({
    cell: { 
        width: "auto", 
        whiteSpace: "nowrap", 
        magin: 5,
        backgroundColor: "#9eb0ff"
    },
    root: {
        flexGrow: 1
    },
    tableContainer: {
        marginRight: "auto",
        marginLeft: "auto",
        minWidth: 500,
        marginBottom: 50
    }
  });


const StyledTableRow = withStyles(theme => ({
    root: {
        '&:nth-of-type(odd)': {
        backgroundColor: theme.palette.background.default,
        }
    }
}))(TableRow);


const scalePrice = (x) => {
    if ( x <= 20 ) {
        return 25000 * x;
    }
    else if ( 20 < x && x <= 30 ) {
        return 500000 + (x - 20) * 50000
    }
    else if ( 30 < x && x <= 39 ) {
        return 1000000 + (x - 30) * 1000000
    }
    else if ( 39 < x && x <= 48 ) {
        return 10000000 + (x - 39) * 10000000
    }
}


const scaleTerrain = (x) => {
    if ( x <= 30 ) {
        return x/2;
    }
    else if ( 30 < x && x <= 45 ) {
        return 15 + (x - 30)
    }
    else if ( 45 < x && x <= 53 ) {
        return 30 + (x - 45) * 2.5
    }
    else if ( 53 < x && x <= 73 ) {
        return 50 + (x - 53) * 5
    }
}


const scaleMagicRatio = (x) => {
    if ( x <= 10 ) {
        return -100 + x * 5;
    }
    else if ( 10 < x && x <= 16 ) {
        return -50 + (x - 10) * 2.5
    }
    else if ( 16 < x && x <= 36 ) {
        return -35 + (x - 16)
    }
    else if ( 36 < x && x <= 42 ) {
        return -15 + (x - 36) * 2.5
    }
    else if ( 42 < x && x <= 48 ) {
        return (x - 42) * 5
    }
    else if ( 48 < x && x <= 55 ) {
        return 30 + (x - 48) * 10
    }
}


function OffersTable() {
    const classes = useStyles();

    const [offers, setOffers] = useState([])
    const [geolocations, setGeolocations] = useState([{type: "country", name: "lu", country: "lu"}])
    const [propertyTypes, setPropertyTypes] = useState([])
    const [orderBy, setOrderBy] = useState('date')
    const [order, setOrder] = useState('desc')
    const [price, setPrice] = React.useState([0, 48]);
    const [surface, setSurface] = React.useState([0, 300]);
    const [terrain, setTerrain] = React.useState([0, 73]);
    const [pricePerM2, setPricePerM2] = React.useState([0, 12000]);
    const [pricePerAre, setPricePerAre] = React.useState([0, 1000000]);
    const [magicRatio, setMagicRatio] = React.useState([0, 36]);
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [emptyRows, setEmptyRows] = React.useState(0);

    useEffect(() => {
        const newValue = rowsPerPage - Math.min(rowsPerPage, offers.length - page * rowsPerPage); 
        setEmptyRows(newValue);
    }, [rowsPerPage, offers, page]);

    useEffect(() => {
        filterAndSort()
        // eslint-disable-next-line
    }, [order, orderBy])

    const formatDate = (timestamp) => {
        // Create a new JavaScript Date object based on the timestamp
        // multiplied by 1000 so that the argument is in milliseconds, not seconds.
        const date = new Date(timestamp * 1000);
        // Hours part from the timestamp
        const hours = date.getHours();
        // Minutes part from the timestamp
        const minutes = "0" + date.getMinutes();
        // Seconds part from the timestamp
        const seconds = "0" + date.getSeconds();
        // Day part from the timestamp
        const day = "0" + date.getDay();
        // Month part from the timestamp
        const month = "0" + date.getMonth();
        // Year part from the timestamp
        const year = "0" + date.getFullYear();


        // Will display time in 10:30:23 format
        const formattedTime = day.substr(-2) + '/' + month.substr(-2) + '/' + year.substr(-2) + ' ' 
                                + hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

        return formattedTime
    }

    const filterAndSort = () => {
        let parameters = {
            priceMin: scalePrice(price[0]),
            priceMax: scalePrice(price[1]),
            surfaceMin: surface[0],
            surfaceMax: surface[1],
            groundSurfaceMin: scaleTerrain(terrain[0]),
            groundSurfaceMax: scaleTerrain(terrain[1]),
            pricePerM2Min: pricePerM2[0],
            pricePerM2Max: pricePerM2[1],
            pricePerAreMin: pricePerAre[0],
            pricePerAreMax: pricePerAre[1],
            magicRatioMin: scaleMagicRatio(magicRatio[0]),
            magicRatioMax: scaleMagicRatio(magicRatio[1]),
            propertyTypes: propertyTypes,
            sort: orderBy,
            sortOrder: order
        }
        const offersUri = process.env.REACT_APP_OFFERS_URI
        axios.post(offersUri, geolocations, {params: parameters})
            .then(function (response) {
                setOffers(response.data);
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
        setPage(0);
    }

    const onRequestSort = (event, newOrderBy) => {
        const isAsc = orderBy === newOrderBy && order === 'asc'
        setOrder( isAsc ? 'desc' : 'asc')
        setOrderBy(newOrderBy)
    }
    
    const sortHandler = (property) => (event) => {
        onRequestSort(event, property);
    };

    const handlePriceChange = (event, newValue) => {
        setPrice(newValue);
    };

    const handleSurfaceChange = (event, newValue) => {
        setSurface(newValue);
    };

    const handleTerrainChange = (event, newValue) => {
        setTerrain(newValue);
    };

    const handlePricePerM2Change = (event, newValue) => {
        setPricePerM2(newValue);
    };

    const handlePricePerAreChange = (event, newValue) => {
        setPricePerAre(newValue);
    };

    const handleMagicRatioChange = (event, newValue) => {
        setMagicRatio(newValue);
    };

    const handleChangePage = (event, newPage) => {
      setPage(newPage);
    };
  
    const handleChangeRowsPerPage = (event) => {
      setRowsPerPage(parseInt(event.target.value, 10));
      setPage(0);
    };

    // object to create table header with map (clean)
    const headCells = [
        { id: 'date', label: 'Date', type: 'icon', sortable: true},
        { id: 'title', label: 'Titre', type: 'text', sortable: false},
        { id: 'city', label: 'Ville', type: 'text', sortable: true},
        { id: 'price', label: 'Prix (€)', type: 'numeric', sortable: true},
        { id: 'surface', label: 'Surface (m²)', type: 'numeric', sortable: true},
        { id: 'pricePerM2', label: 'Prix au m² (€/m²)', type: 'numeric', sortable: true},
        { id: 'groundSurface', label: 'Terrain (ares)', type: 'numeric', sortable: true},
        { id: 'pricePerAre', label: 'Prix de l\'are (€/are)', type: 'numeric', sortable: true},
        { id: 'ratio', label: 'Ratio magique (%)', type: 'numeric', sortable: true},
        { id: 'relevance', label: 'Pertinence', type: 'text', sortable: false},
        { id: 'mapsLink', label: 'Maps', type: 'icon', sortable: false},
        { id: 'offerLink', label: 'Annonce', type: 'icon', sortable: false}
    ];

    return (
        <div style={{width: "90%", margin: "0 auto"}}>
            <div style={{display: 'flex', marginTop: 25, marginBottom: 15}}>
                <Grid container className={classes.root} spacing={2}>
                    <Grid container direction='row'>
                        <Grid item xs={8} lg={6} style={{paddingRight: 20}}>
                            <GeoEntryField onChangeFunc={setGeolocations} />
                        </Grid>
                        <Grid item xs={8} lg={6}>
                            <PropertyTypeField onChangeFunc={setPropertyTypes} />
                        </Grid>
                    </Grid>

                    <Grid container direction='row' style={{marginTop: 20}}>
                        <Grid item xs={8} lg={6} key={1} style={{paddingLeft: 20}}>
                            <PriceSlider price={price} handlePriceChange={handlePriceChange} scaleFunc={scalePrice}/>
                        </Grid>
                        <Grid item xs={8} lg={6} key={2} style={{paddingLeft: 20}}>
                            <PricePerM2Slider pricePerM2={pricePerM2} handlePricePerM2Change={handlePricePerM2Change} />
                        </Grid>
                    </Grid>

                    <Grid container direction='row' style={{marginTop: 20}}>
                        <Grid item xs={8} lg={6} key={3} style={{paddingLeft: 20}}>
                            <SurfaceSlider surface={surface} handleSurfaceChange={handleSurfaceChange}/>
                        </Grid>
                        <Grid item xs={8} lg={6} key={4} style={{paddingLeft: 20}}>
                            <PricePerAreSlider pricePerAre={pricePerAre} handlePricePerAreChange={handlePricePerAreChange}/>
                        </Grid>
                    </Grid>

                    <Grid container direction='row' style={{marginTop: 20}}>
                        <Grid item xs={8} lg={6} key={5} style={{paddingLeft: 20}}>
                            <TerrainSlider terrain={terrain} handleTerrainChange={handleTerrainChange} scaleFunc={scaleTerrain}/>
                        </Grid>
                        <Grid item xs={8} lg={6} key={6} style={{paddingLeft: 20}}>
                            <MagicRatioSlider magicRatio={magicRatio} handleMagicRatioChange={handleMagicRatioChange} scaleFunc={scaleMagicRatio}/>
                        </Grid>
                    </Grid>

                    <Grid container alignItems="flex-start" justify="flex-end" direction="row">
                        <Button 
                            variant="contained" 
                            color="primary" 
                            style={{ margin: 20, maxHeight: 50 }}
                            onClick={() => filterAndSort()}>
                            Chercher
                        </Button>
                    </Grid>
                </Grid>
            </div>
            <Paper className={classes.tableContainer}>
                <Table stickyHeader>
                    <TableHead> 
                    <TableRow>
                        {headCells.map(headCell => (
                            <TableCell 
                                key={headCell.id} 
                                className={classes.cell}
                                align={headCell.type === 'icon' ? 'center' : (headCell.type === 'text' ? 'left' : 'right')}
                            >
                                {
                                    headCell.sortable 
                                        ?   <TableSortLabel
                                                active={orderBy === headCell.id}
                                                direction={orderBy === headCell.id ? order : 'asc'}
                                                onClick={sortHandler(headCell.id)}
                                            >
                                                {headCell.label}
                                            </TableSortLabel>
                                        : headCell.label
                                }
                            </TableCell>
                        ))}
                    </TableRow>
                    </TableHead>
                    <TableBody className={classes.tableBody}>
                    {(rowsPerPage > 0
                        ? offers.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                        : offers
                     ).map(row => (
                        <StyledTableRow key={offers.indexOf(row)}>
                            <TableCell align="center">
                                <Tooltip title={formatDate(row.insertion_date)}>
                                    <AccessTimeIcon/>
                                </Tooltip>
                            </TableCell>
                            <TableCell align="left">{row.title}</TableCell>
                            <TableCell align="left">{row.city}</TableCell>
                            <TableCell align="right">{row.price.toLocaleString("fr-FR")}</TableCell>
                            <TableCell align="right">{row.surface}</TableCell>
                            <TableCell align="right">{parseFloat(row.price_per_m2).toLocaleString("fr-FR", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</TableCell>
                            <TableCell align="right">{row.ground_surface}</TableCell>
                            <TableCell align="right">{parseFloat(row.price_per_are).toLocaleString("fr-FR", {minimumFractionDigits: 2, maximumFractionDigits: 2})}</TableCell>
                            <TableCell align="right">{(row.magic_ratio > 0 ? "+" : "").concat(`${parseFloat(row.magic_ratio).toLocaleString("fr-FR", {minimumFractionDigits: 2, maximumFractionDigits: 2}).toLocaleString()} %`)}</TableCell>
                            <TableCell align="left">{row.pertinence}</TableCell>
                            <TableCell align="center"><a href={row.maps_link} target="_blank" rel="noopener noreferrer"><RoomIcon/> </a></TableCell>
                            <TableCell align="center"><a href={row.url} target="_blank" rel="noopener noreferrer"><HomeTwoToneIcon/> </a></TableCell>
                        </StyledTableRow>
                    ))}

                    {emptyRows > 0 && (
                        <TableRow style={{ height: 53 * emptyRows }}>
                        <TableCell colSpan={6} />
                        </TableRow>
                    )}
                    </TableBody>
                    <TableFooter>
                        <TableRow style={{backgroundColor: "#edf0ff"}}>
                            <TablePagination
                            rowsPerPageOptions={[10, 20, 30, { label: 'All', value: -1 }]}
                            colSpan={12}
                            count={offers.length}
                            rowsPerPage={rowsPerPage}
                            page={page}
                            SelectProps={{
                                inputProps: { 'aria-label': 'rows per page' },
                                native: true,
                            }}
                            onChangePage={handleChangePage}
                            onChangeRowsPerPage={handleChangeRowsPerPage}
                            ActionsComponent={TablePaginationActions}
                            />
                        </TableRow>
                    </TableFooter>
                </Table>
                </Paper>
        </div>
    )
}

export default OffersTable;