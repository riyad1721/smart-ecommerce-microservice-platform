import { Menu, ShoppingBag } from 'lucide-react';
import Button from '../common/Button';
import { clearAuth } from '../../utils/token';
import { useNavigate } from 'react-router-dom';

const Navbar = ({ onMenuClick }: { onMenuClick?: () => void }) => {
  const navigate = useNavigate();
  const logout = () => {
    clearAuth();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
      <div className="flex h-16 items-center justify-between px-4 lg:px-8">
        <div className="flex items-center gap-3">
          <button className="rounded-xl p-2 hover:bg-slate-100 lg:hidden" onClick={onMenuClick}>
            <Menu className="h-5 w-5" />
          </button>
          <div className="flex items-center gap-2 font-bold text-slate-900">
            <span className="rounded-xl bg-blue-600 p-2 text-white"><ShoppingBag className="h-5 w-5" /></span>
            Smart E-Commerce
          </div>
        </div>
        <Button variant="ghost" onClick={logout}>Logout</Button>
      </div>
    </header>
  );
};

export default Navbar;
