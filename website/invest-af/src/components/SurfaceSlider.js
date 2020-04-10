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
        label: '0 m²',
    },
    {
        value: 50,
        label: '50 m²',
    },
    {
        value: 100,
        label: '100 m²',
    },
    {
        value: 200,
        label: '200 m²',
    },
    {
        value: 300,
        label: '300+ m²',
    }
];


function SurfaceSlider(props) {

    const { surface, handleSurfaceChange } = props;

    return (
        <>
            <Typography id="range-slider" gutterBottom>
                Surface 
            </Typography>
            <Slider
                style={{maxWidth: 500}}
                min={0}
                step={1}
                max={300}
                marks={marks}
                value={surface}
                onChange={handleSurfaceChange}
                valueLabelDisplay="auto"
                valueLabelFormat={ (x) => x === 300 ? `${x}+ m²` : `${x} m²` }
                ValueLabelComponent={ValueLabelComponent}
            />
        </>
    )
}

SurfaceSlider.propTypes = {
    surface: PropTypes.array.isRequired,
    handleSurfaceChange: PropTypes.func.isRequired
};

export default SurfaceSlider
