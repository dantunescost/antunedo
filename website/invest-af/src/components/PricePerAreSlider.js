import React from 'react'
import Typography from '@material-ui/core/Typography';
import Tooltip from '@material-ui/core/Tooltip';
import Slider from '@material-ui/core/Slider';
import PropTypes from 'prop-types';

function ValueLabelComponent(props) {
    const { children, open, value } = props;
  
    return (
      <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
        {children}
      </Tooltip>
    );
}
  
ValueLabelComponent.propTypes = {
    children: PropTypes.element.isRequired,
    open: PropTypes.bool.isRequired,
    value: PropTypes.string.isRequired,
};


const marks = [
    {
        value: 0,
        label: '0 €/are',
    },
    {
        value: 250000,
        label: '250k €/are',
    },
    {
        value: 500000,
        label: '500k €/are',
    },
    {
        value: 750000,
        label: '750k €/are',
    },
    {
        value: 1000000,
        label: '1M+ €/are',
    }
];


function PricePerAreSlider(props) {

    const { pricePerAre, handlePricePerAreChange } = props;

    return (
        <>
            <Typography id="range-slider" gutterBottom>
                Prix de l'are 
            </Typography>
            <Slider
                style={{maxWidth: 500}}
                min={0}
                step={5000}
                max={1000000}
                marks={marks}
                value={pricePerAre}
                onChange={handlePricePerAreChange}
                valueLabelDisplay="auto"
                valueLabelFormat={ (x) => x === 1000000 ? `${x.toLocaleString("fr-FR")}+ €/are` : `${x.toLocaleString("fr-FR")} €/are`}
                ValueLabelComponent={ValueLabelComponent}
            />
        </>
    )
}

PricePerAreSlider.propTypes = {
    pricePerAre: PropTypes.array.isRequired,
    handlePricePerAreChange: PropTypes.func.isRequired
};

export default PricePerAreSlider
