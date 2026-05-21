import { Link, useNavigate } from 'react-router-dom';
import { useState, type FormEvent } from 'react';
import toast from 'react-hot-toast';
import { loginApi } from '../../api/authApi';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

const LoginPage = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const getLoginErrorMessage = (error: unknown): string => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const axiosError = error as {
        response?: {
          data?: {
            detail?: unknown;
          };
        };
      };

      const detail = axiosError.response?.data?.detail;

      if (typeof detail === 'string') {
        return detail;
      }

      if (Array.isArray(detail)) {
        return detail
          .map((item) => {
            if (typeof item === 'object' && item !== null && 'msg' in item) {
              return String((item as { msg: unknown }).msg);
            }

            return String(item);
          })
          .join(', ');
      }
    }

    return 'Login failed. Please check your email and password.';
  };

  const submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!email.trim()) {
      toast.error('Email is required');
      return;
    }

    if (!password) {
      toast.error('Password is required');
      return;
    }

    setLoading(true);

    try {
      const response = await loginApi({
        email: email.trim(),
        password,
      });

      const token =
        response.data?.access_token ||
        response.data?.token ||
        response.data?.accessToken;

      if (!token) {
        toast.error('Login successful but token not found in response');
        console.log('Login response:', response.data);
        return;
      }

      localStorage.setItem('token', token);

      if (response.data?.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }

      toast.success('Login successful');
      navigate('/', { replace: true });
    } catch (error) {
      toast.error(getLoginErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-screen place-items-center bg-gradient-to-br from-slate-100 via-white to-blue-50 p-4">
      <form
        onSubmit={submit}
        className="w-full max-w-md rounded-3xl bg-white p-8 shadow-soft"
      >
        <p className="text-sm font-semibold text-blue-600">
          Welcome back
        </p>

        <h1 className="mt-2 text-3xl font-bold text-slate-900">
          Login
        </h1>

        <div className="mt-8 space-y-4">
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="user@example.com"
          />

          <Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Enter password"
          />

          <Button className="w-full" loading={loading}>
            Login
          </Button>
        </div>

        <p className="mt-6 text-center text-sm text-slate-500">
          Do not have account?{' '}
          <Link className="font-semibold text-blue-600" to="/register">
            Register
          </Link>
        </p>
      </form>
    </div>
  );
};

export default LoginPage;