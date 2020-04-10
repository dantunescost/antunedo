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
        label: '0€',
    },
    {
        value: 6,
        label: '150k€',
    },
    {
        value: 20,
        label: '500k€',
    },
    {
        value: 30,
        label: '1M€',
    },
    {
        value: 39,
        label: '10M€',
    },
    {
        value: 48,
        label: '100M€',
    }
];


function PriceSlider(props) {

    const { price, handlePriceChange, scaleFunc } = props;

    return (
        <>
            <Typography id="range-slider" gutterBottom>
                Prix 
            </Typography>
            <Slider
                style={{maxWidth: 500}}
                min={0}
                step={1}
                max={48}
                scale={(x) => scaleFunc(x)}
                marks={marks}
                value={price}
                onChange={handlePriceChange}
                valueLabelDisplay="auto"
                valueLabelFormat={ (x) => `${x.toLocaleString("fr-FR")}€` }
                ValueLabelComponent={ValueLabelComponent}
            />
        </>
    )
}

PriceSlider.propTypes = {
    price: PropTypes.array.isRequired,
    handlePriceChange: PropTypes.func.isRequired,
    scaleFunc: PropTypes.func.isRequired
};

export default PriceSlider
