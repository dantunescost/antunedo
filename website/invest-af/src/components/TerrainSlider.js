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
        label: '0 ares',
    },
    {
        value: 20,
        label: '10 ares',
    },
    {
        value: 40,
        label: '25 ares',
    },
    {
        value: 53,
        label: '50 ares',
    },
    {
        value: 73,
        label: '150+ ares',
    }
];


function TerrainSlider(props) {

    const { terrain, handleTerrainChange, scaleFunc } = props;

    return (
        <>
            <Typography id="range-slider" gutterBottom>
                Terrain 
            </Typography>
            <Slider
                style={{maxWidth: 500}}
                min={0}
                step={1}
                max={73}
                marks={marks}
                value={terrain}
                scale={scaleFunc}
                onChange={handleTerrainChange}
                valueLabelDisplay="auto"
                valueLabelFormat={ (x) => x === 1 ? `${x} are` : x === 150 ? `${x}+ ares` : `${x} ares`}
                ValueLabelComponent={ValueLabelComponent}
            />
        </>
    )
}

TerrainSlider.propTypes = {
    terrain: PropTypes.array.isRequired,
    handleTerrainChange: PropTypes.func.isRequired,
    scaleFunc: PropTypes.func.isRequired
};

export default TerrainSlider
