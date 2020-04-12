import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import countries from '../data/countries';
import https from 'https';
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';

const useStyles = makeStyles({
    option: {
      fontSize: 15,
      '& > span': {
        marginRight: 10,
        fontSize: 18,
      }
    }
  });


function countryToFlag(isoCode) {
    return typeof String.fromCodePoint !== 'undefined'
        ? isoCode.toUpperCase().replace(/./g, char => String.fromCodePoint(char.charCodeAt(0) + 127397))
        : isoCode;
}

const GeoEntryField = (props) => {

    const { onChangeFunc } = props;

    const [options, setOptions] = useState([])

    const classes = useStyles()

    useEffect(() => {
        const geoOptionsUri = process.env.REACT_APP_GEO_OPTIONS_URI
        const agent = new https.Agent({  
            rejectUnauthorized: false
          });
        axios.get(geoOptionsUri, { httpsAgent: agent })
            .then(function (response) {
                setOptions(response.data);
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
    }, [])
    
    return (
        <Autocomplete
            id='geolocation-search'
            style={{ minWidth: 500, maxWidth: 700}}
            options={options}
            classes={{
                option: classes.option,
            }}
            autoHighlight
            multiple
            defaultValue={[{type: "country", name: "lu", country: "lu"}]}
            getOptionLabel={option => 
                option.type === 'country' ? countries.find(c => {return c.code === option.name.toUpperCase()}).label : option.name
            }
            renderOption={option => {
                if(option.type === 'country'){
                    return (
                        <>
                        <span>{countryToFlag(option.country)}</span>
                        {countries.find(c => {return c.code === option.name.toUpperCase()}).label}&nbsp;
                        ({option.country.toUpperCase()})
                        </>
                        )
                } else {
                    let typeDeGeo = ""
                    switch(option.type) {
                        case 'city':
                            typeDeGeo = "ville"
                            break;
                        case 'L4':
                            typeDeGeo = "région"
                            break;
                        case 'L5':
                            typeDeGeo = "département"
                            break;
                        case 'L7':
                            typeDeGeo = "commune"
                            break;
                        case 'L10':
                            typeDeGeo = "quartier"
                            break;
                        default:
                            break;
                      }
                    return (
                        <>
                        {option.name} ({typeDeGeo} {countryToFlag(option.country)})
                        </>
                        )
                }
            }}
            onChange={(e, value) => onChangeFunc(value)}
            renderInput={params => (
                <TextField
                {...params}
                label="Pays, région, commune, ville, ..."
                variant="outlined"
                inputProps={{
                    ...params.inputProps,
                    autoComplete: 'new-password', // disable autocomplete and autofill
                }}
                />
            )}
        />
    );
};

GeoEntryField.propTypes = {
    onChangeFunc: PropTypes.func
};

export default GeoEntryField;