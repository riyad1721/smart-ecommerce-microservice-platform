import { useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import { createOrder, getCart, removeCartItem } from '../../api/orderApi';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import EmptyState from '../../components/common/EmptyState';
import Loader from '../../components/common/Loader';
import type { Cart, CartItem } from '../../types/cart';
import { formatCurrency, getErrorMessage } from '../../utils/format';

const itemTotal = (item: CartItem) => Number(item.total_price ?? item.price ?? 0) * (item.total_price ? 1 : item.quantity);

const CartPage = () => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [ordering, setOrdering] = useState(false);

  const total = useMemo(() => Number(cart?.total ?? cart?.total_amount ?? cart?.items?.reduce((sum, item) => sum + itemTotal(item), 0) ?? 0), [cart]);

  const loadCart = async () => {
    setLoading(true);
    try { setCart(await getCart()); } catch (error) { toast.error(getErrorMessage(error)); } finally { setLoading(false); }
  };
  useEffect(() => { void loadCart(); }, []);

  const removeItem = async (id: string) => {
    try { await removeCartItem(id); toast.success('Item removed'); await loadCart(); } catch (error) { toast.error(getErrorMessage(error)); }
  };

  const placeOrder = async () => {
    setOrdering(true);
    try { await createOrder(); toast.success('Order created successfully'); await loadCart(); } catch (error) { toast.error(getErrorMessage(error)); } finally { setOrdering(false); }
  };

  if (loading) return <Loader />;
  if (!cart?.items?.length) return <EmptyState title="Cart is empty" message="Add products to cart first." />;

  return (
    <section className="space-y-5">
      <div><h1 className="text-2xl font-bold text-slate-900">Cart</h1><p className="text-sm text-slate-500">Review cart items and create order.</p></div>
      <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
        <div className="space-y-3">
          {cart.items.map((item) => {
            const id = item.item_id || item.id;
            return <Card key={id} className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
              <div><h3 className="font-bold text-slate-900">{item.product?.name || item.product_name || item.product_id}</h3><p className="text-sm text-slate-500">Qty: {item.quantity}</p></div>
              <div className="flex items-center gap-3"><span className="font-bold">{formatCurrency(itemTotal(item))}</span><Button variant="danger" onClick={() => removeItem(id)}>Remove</Button></div>
            </Card>;
          })}
        </div>
        <Card className="h-fit"><h2 className="text-lg font-bold">Cart Summary</h2><div className="mt-4 flex justify-between text-sm"><span>Total</span><b>{formatCurrency(total)}</b></div><Button className="mt-6 w-full" loading={ordering} onClick={placeOrder}>Create Order</Button></Card>
      </div>
    </section>
  );
};

export default CartPage;
