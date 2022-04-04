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
        label: '-100%',
    },
    {
        value: 16,
        label: '-35%',
    },
    {
        value: 31,
        label: '-20%',
    },
    {
        value: 42,
        label: '0%',
    },
    {
        value: 55,
        label: '+100%',
    }
];


function MagicRatioSlider(props) {

    const { magicRatio, handleMagicRatioChange, scaleFunc } = props;

    return (
        <>
            <Typography id="range-slider" gutterBottom>
                Ratio magique 
            </Typography>
            <Slider
                style={{maxWidth: 500}}
                min={0}
                step={1}
                max={55}
                scale={(x) => scaleFunc(x)}
                marks={marks}
                value={magicRatio}
                onChange={handleMagicRatioChange}
                valueLabelDisplay="auto"
                valueLabelFormat={ (x) => x > 0 ? `+${x.toLocaleString("fr-FR")}%`: `${x.toLocaleString("fr-FR")}%` }
                ValueLabelComponent={ValueLabelComponent}
            />
        </>
    )
}

MagicRatioSlider.propTypes = {
    magicRatio: PropTypes.array.isRequired,
    handleMagicRatioChange: PropTypes.func.isRequired,
    scaleFunc: PropTypes.func.isRequired
};

export default MagicRatioSlider
