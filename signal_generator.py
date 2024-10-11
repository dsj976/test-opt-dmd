import numpy as np


class SignalGenerator:
    """
    A class to generate synthetic spatio-temporal signals.

    Attributes
    ----------
    nx : int
        Number of spatial points. Default is 100.
    nt : int
        Number of temporal points. Default is 500.
    x_min : float
        Minimum spatial coordinate. Default is 0.
    x_max : float
        Maximum spatial coordinate. Default is 10.
    t_min : float
        Minimum temporal coordinate. Default is 0.
    t_max : float
        Maximum temporal coordinate. Default is 50.
    x : np.ndarray
        Spatial coordinate vector with shape (nx,)
    t : np.ndarray
        Temporal coordinate vector with shape (nt,)
    X : np.ndarray
        Spatial coordinate matrix with shape (nt, nx)
    T : np.ndarray
        Temporal coordinate matrix with shape (nt, nx)
    signal : np.ndarray
        Synthesized spatio-temporal signal with shape (nt, nx)
    components : list
        List of dictionaries containing the signal components

    Methods
    -------
    add_sinusoid1(a=1, k=0.1, omega=1, gamma=0)
        Generate a sinusoidal signal of the form: a*sin(k*x - omega*t)*exp(gamma*t)
    add_sinusoid2(a=1, k=0.2, omega=1, c=0)
        Generate a sinusoidal signal of the form: a*(exp(-k*(x+c)^2)*cos(omega*t)
    add_trend(mu=0.2, trend=0.01)
        Generate a linear trend in time of the form: mu + trend*t
    add_noise(noise_std=0.1, random_seed=None)
        Add Gaussian noise to the signal.

    """

    def __init__(
            self,
            nx=100,
            nt=500,
            x_min=0,
            x_max=10,
            t_min=0,
            t_max=50,
    ):
        self.x = np.linspace(x_min, x_max, nx)
        self.t = np.linspace(t_min, t_max, nt)
        self.X, self.T = np.meshgrid(self.x, self.t)
        self.signal = np.zeros(self.X.shape)
        self.components = []

    def add_sinusoid1(self, a=1, k=0.1, omega=1, gamma=0):
        """
        Generate a sinusoidal signal of the form: a*sin(k*x - omega*t)*exp(gamma*t)

        Parameters
        ----------
        a : float, optional
            Amplitude of the sinusoidal signal, by default 1
        k : float, optional
            Spatial frequency of the signal, by default 0.1
        omega : float, optional
            Temporal frequency of the signal, by default 1
        gamma : float, optional
            Temporal decay rate of the signal, by default 0
        """
        signal = np.sin(k*self.X - omega*self.T)*np.exp(gamma*self.T)
        spatial_norm = np.linalg.norm(signal, axis=-1, ord=2)
        signal = signal / spatial_norm[:, None]
        signal = a * signal
        my_dict = {'type': 'sinusoid1', 'a': a, 'k': k, 'omega': omega, 'gamma': gamma, 'signal': signal}
        self.components.append(my_dict)
        self.signal += signal

    def add_sinusoid2(self, a=1, k=0.2, omega=1, c=0):
        """
        Generate a sinusoidal signal of the form: a*(exp(-k*(x+c)^2)*cos(omega*t)

        Parameters
        ----------
        a : float, optional
            Amplitude (area under the curve) of the signal, by default 1
        k : float, optional
            Spatial exponential decay rate of the signal, by default 0.2
        omega : float, optional
            Temporal frequency of the signal, by default 1
        c : float, optional
            Offset of the signal, by default 0
        """
        spatial_signal = np.exp(-k*(self.X+c)**2)
        area = np.trapz(spatial_signal, self.x, axis=-1)[0]  # Compute the area under the curve
        signal = a * spatial_signal / area * np.cos(omega*self.T)
        my_dict = {'type': 'sinusoid2', 'a': a, 'k': k, 'omega': omega, 'c': c, 'signal': signal}
        self.components.append(my_dict)
        self.signal += signal

    def add_trend(self, mu=0.2, trend=0.01):
        """
        Generate a linear trend in time of the form: mu + trend*t

        Parameters
        ----------
        mu : float, optional
            Initial value of the trend, by default 0.2
        trend : float, optional
            Slope of the trend, by default 0.01
        """
        signal = self.T*trend + mu
        my_dict = {'type': 'trend', 'mu': mu, 'trend': trend, 'signal': signal}
        self.components.append(my_dict)
        self.signal += signal

    def add_noise(self, noise_std=0.1, random_seed=None):
        """
        Add Gaussian noise to the signal.

        Parameters
        ----------
        noise_std : float, optional
            Standard deviation of the Gaussian noise, by default 0.1
        random_seed : int, optional
            Random seed for reproducibility, by default None
        """
        np.random.seed(random_seed)
        self.signal += np.random.normal(0, noise_std, self.signal.shape)
