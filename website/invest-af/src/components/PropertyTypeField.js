import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
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

const PropertyTypeField = (props) => {

    const { onChangeFunc } = props;

    const [options, setOptions] = useState([])

    const classes = useStyles()

    useEffect(() => {
        const propertyTypeURI = process.env.REACT_APP_PROPERTY_TYPES_URI
        axios.get(propertyTypeURI)
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
            id='property-type-filter'
            style={{ minWidth: 200, maxWidth: 500}}
            options={options}
            classes={{
                option: classes.option,
            }}
            autoHighlight
            multiple
            getOptionLabel={option => option}
            renderOption={option => option}
            onChange={(e, value) => onChangeFunc(value)}
            renderInput={params => (
                <TextField
                {...params}
                label="Types de biens"
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

PropertyTypeField.propTypes = {
    onChangeFunc: PropTypes.func
};

export default PropertyTypeField;