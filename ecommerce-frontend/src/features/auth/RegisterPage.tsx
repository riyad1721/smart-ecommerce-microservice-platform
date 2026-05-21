import { Link, useNavigate } from 'react-router-dom';
import { useState, type FormEvent } from 'react';
import toast from 'react-hot-toast';
import { registerApi } from '../../api/authApi';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

const RegisterPage = () => {
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const getRegisterErrorMessage = (error: unknown): string => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
      const axiosError = error as {
        response?: {
          data?: {
            detail?: unknown;
          };
        };
      };

      const detail = axiosError.response?.data?.detail;

      if (Array.isArray(detail)) {
        return detail
          .map((item) => {
            if (typeof item === 'object' && item !== null && 'msg' in item) {
              const validationItem = item as { loc?: unknown; msg: unknown };
              const field =
                Array.isArray(validationItem.loc) &&
                validationItem.loc.length > 0
                  ? String(validationItem.loc[validationItem.loc.length - 1])
                  : '';

              return field
                ? `${field}: ${String(validationItem.msg)}`
                : String(validationItem.msg);
            }

            return String(item);
          })
          .join(', ');
      }

      if (typeof detail === 'string') {
        return detail;
      }
    }

    return 'Registration failed. Please check your input.';
  };

  const submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!name.trim()) {
      toast.error('Name is required');
      return;
    }

    if (name.trim().length < 2) {
      toast.error('Name must be at least 2 characters');
      return;
    }

    if (name.trim().length > 150) {
      toast.error('Name must be 150 characters or fewer');
      return;
    }

    if (!email.trim()) {
      toast.error('Email is required');
      return;
    }

    if (password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }

    if (password.length > 100) {
      toast.error('Password must be 100 characters or fewer');
      return;
    }

    setLoading(true);

    try {
      await registerApi({
        full_name: name.trim(),
        email: email.trim().toLowerCase(),
        password,
      });

      toast.success('Registration successful. Please login.');
      navigate('/login');
    } catch (error) {
      toast.error(getRegisterErrorMessage(error));
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
          Create account
        </p>

        <h1 className="mt-2 text-3xl font-bold text-slate-900">
          Register
        </h1>

        <div className="mt-8 space-y-4">
          <Input
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            minLength={2}
            maxLength={150}
            placeholder="Md Reyad Hossain"
          />

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
            minLength={6}
            maxLength={100}
            placeholder="Minimum 6 characters"
          />

          <Button className="w-full" loading={loading}>
            Register
          </Button>
        </div>

        <p className="mt-6 text-center text-sm text-slate-500">
          Already have account?{' '}
          <Link className="font-semibold text-blue-600" to="/login">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
};

export default RegisterPage;
