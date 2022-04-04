import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
// import FormControlLabel from '@material-ui/core/FormControlLabel';
// import Checkbox from '@material-ui/core/Checkbox';
// import Link from '@material-ui/core/Link';
// import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import axios from 'axios';
import Cookies from 'js-cookie';
import {Redirect} from 'react-router-dom';


function MadeWithLove() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Built with love by the Invest AF team.'}
    </Typography>
  );
}

const useStyles = makeStyles(theme => ({
  '@global': {
    body: {
      backgroundColor: theme.palette.common.white,
    },
  },
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

function SignIn(props) {
  const classes = useStyles();

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const signIn = (u, p, e) => {
    const uri = process.env.REACT_APP_SIGN_IN_URI
    axios.post(`${uri}?username=${u}&password=${p}`)
      .then(response => {
        if(response.data){
            Cookies.set('fb_2NyPcDJq15wTar35ZR', 'true', { expires: 1/24 })
            props.history.push('/dashboard')
        }
        else {
            Cookies.set('fb_2NyPcDJq15wTar35ZR', 'false')
            props.history.push('/')
        }

      })
      .catch( error => {
        console.log(error)
      })
    e.preventDefault()
  }

  if(Cookies.get('fb_2NyPcDJq15wTar35ZR') === 'true'){
      return <Redirect to="/dashboard" />;
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form} noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            autoFocus
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id="password"
            autoComplete="current-password"
          />
          { /* <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"/> */}  
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            onClick={(e) => signIn(username, password, e)}>
            Sign In
          </Button>
          {/*<Grid container>
            <Grid item xs>
              <Link href="#" variant="body2" onClick={forgotPasswordLinkHandler}>
                Forgot password?
              </Link>
            </Grid>
             <Grid item>
                <Link href="#" variant="body2">
                {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>*/}
        </form>
      </div>
      <Box mt={5}>
        <MadeWithLove />
      </Box>
    </Container>
  );
}

export default SignIn
