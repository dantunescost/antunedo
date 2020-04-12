import React from 'react';
import PropTypes from 'prop-types';
import { Route, Redirect } from 'react-router-dom';
import Cookies from 'js-cookie';

export default function PrivateRoute({
    component: Component,
    isPrivate,
    ...rest
}) {

    const signed = Cookies.get('tao') === 'true'
    
    // TODO : Add duration to cookie
    
    /**
    * Redirect user to SignIn page if he tries to access a private route
    * without authentication.
    */
    if (isPrivate && !signed) {
        return <Redirect to="/" />;
    }
    /**
    * Redirect user to Main page if he tries to access a non private route
    * (SignIn or SignUp) after being authenticated.
    */
    if (!isPrivate && signed) {
        return <Redirect to="/dashboard" />;
    }
    /**
    * If not included on both previous cases, redirect user to the desired route.
    */
    return (<Route 
        {...rest}
        render={props => {
            if (signed){
                return <Component {...props} />;
            } else {
                return (<Redirect to={{
                    pathname: "/",
                    state: {
                        from: props.location
                    }
                }} />)
            }
        }
    } />);
}
PrivateRoute.propTypes = {
    isPrivate: PropTypes.bool,
    component: PropTypes.oneOfType([PropTypes.element, PropTypes.func])
    .isRequired,
};
PrivateRoute.defaultProps = {
    isPrivate: false,
};