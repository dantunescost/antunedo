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
        label: '0 €/m²',
    },
    {
        value: 2000,
        label: '2000 €/m²',
    },
    {
        value: 5000,
        label: '5000 €/m²',
    },
    {
        value: 8000,
        label: '8000 €/m²',
    },
    {
        value: 12000,
        label: '12k+ €/m²',
    }
];


function PricePerM2Slider(props) {

    const { pricePerM2, handlePricePerM2Change } = props;

    return (
        <>
            <Typography id="range-slider" gutterBottom>
                Prix du m² 
            </Typography>
            <Slider
                style={{maxWidth: 500}}
                min={0}
                step={50}
                max={12000}
                marks={marks}
                value={pricePerM2}
                onChange={handlePricePerM2Change}
                valueLabelDisplay="auto"
                valueLabelFormat={ (x) => x === 12000 ? `${x.toLocaleString("fr-FR")}+ €/m²` : `${x.toLocaleString("fr-FR")} €/m²`}
                ValueLabelComponent={ValueLabelComponent}
            />
        </>
    )
}

PricePerM2Slider.propTypes = {
    pricePerM2: PropTypes.array.isRequired,
    handlePricePerM2Change: PropTypes.func.isRequired
};

export default PricePerM2Slider
