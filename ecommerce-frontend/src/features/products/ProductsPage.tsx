import { useEffect, useState, type FormEvent } from 'react';
import { Plus, Save, Search, X } from 'lucide-react';
import toast from 'react-hot-toast';
import {
  createProduct,
  deleteProduct,
  getCategories,
  getProducts,
  searchProducts,
  updateProduct,
} from '../../api/productApi';
import { addToCart } from '../../api/orderApi';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import EmptyState from '../../components/common/EmptyState';
import Input from '../../components/common/Input';
import Loader from '../../components/common/Loader';
import ProductCard from '../../components/product/ProductCard';
import type { Category, Product, ProductPayload } from '../../types/product';
import { getErrorMessage } from '../../utils/format';

type ProductFormState = {
  name: string;
  description: string;
  price: string;
  stock: string;
  category_id: string;
};

const emptyForm: ProductFormState = {
  name: '',
  description: '',
  price: '',
  stock: '',
  category_id: '',
};

const ProductsPage = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [query, setQuery] = useState('');
  const [form, setForm] = useState<ProductFormState>(emptyForm);
  const [editingId, setEditingId] = useState<string | number | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState<string | number | null>(null);

  const loadProducts = async () => {
    setLoading(true);
    try {
      setProducts(query.trim() ? await searchProducts(query.trim()) : await getProducts());
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      setCategories(await getCategories());
    } catch {
      setCategories([]);
    }
  };

  useEffect(() => {
    void loadProducts();
    void loadCategories();
  }, []);

  const handleSearch = (e: FormEvent) => {
    e.preventDefault();
    void loadProducts();
  };

  const handleClearSearch = () => {
    setQuery('');
    setLoading(true);
    getProducts()
      .then(setProducts)
      .catch((error) => toast.error(getErrorMessage(error)))
      .finally(() => setLoading(false));
  };

  const toPayload = (): ProductPayload | null => {
    const name = form.name.trim();
    const price = Number(form.price);
    const stock = Number(form.stock);
    const categoryId = Number(form.category_id);

    if (name.length < 2) {
      toast.error('Product name must be at least 2 characters');
      return null;
    }

    if (!Number.isFinite(price) || price <= 0) {
      toast.error('Price must be greater than 0');
      return null;
    }

    if (!Number.isInteger(stock) || stock < 0) {
      toast.error('Stock must be a whole number 0 or above');
      return null;
    }

    if (!Number.isInteger(categoryId) || categoryId <= 0) {
      toast.error('Category ID is required');
      return null;
    }

    return {
      name,
      description: form.description.trim() || undefined,
      price,
      stock,
      category_id: categoryId,
    };
  };

  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };

  const handleSubmitProduct = async (e: FormEvent) => {
    e.preventDefault();

    const payload = toPayload();
    if (!payload) return;

    setSaving(true);
    try {
      if (editingId) {
        await updateProduct(editingId, payload);
        toast.success('Product updated');
      } else {
        await createProduct(payload);
        toast.success('Product created');
      }

      resetForm();
      await loadProducts();
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setSaving(false);
    }
  };

  const startEdit = (product: Product) => {
    setEditingId(product.id);
    setForm({
      name: product.name,
      description: product.description ?? '',
      price: String(product.price ?? ''),
      stock: String(product.stock ?? ''),
      category_id: String(product.category_id ?? ''),
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (product: Product) => {
    const confirmed = window.confirm(`Delete "${product.name}"?`);
    if (!confirmed) return;

    setDeletingId(product.id);
    try {
      await deleteProduct(product.id);
      toast.success('Product deleted');
      if (editingId === product.id) resetForm();
      await loadProducts();
    } catch (error) {
      toast.error(getErrorMessage(error));
    } finally {
      setDeletingId(null);
    }
  };

  const handleAdd = async (product: Product) => {
    try {
      await addToCart({ product_id: String(product.id), quantity: 1 });
      toast.success(`${product.name} added to cart`);
    } catch (error) {
      toast.error(getErrorMessage(error));
    }
  };

  return (
    <section className="space-y-5">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Products</h1>
          <p className="text-sm text-slate-500">Create, update, delete, and browse products from product-service.</p>
        </div>
        <form onSubmit={handleSearch} className="flex w-full gap-2 md:max-w-md">
          <Input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search products..." />
          <Button variant="secondary"><Search className="h-4 w-4" /> Search</Button>
          {query && <Button type="button" variant="ghost" onClick={handleClearSearch}><X className="h-4 w-4" /></Button>}
        </form>
      </div>

      <Card>
        <form onSubmit={handleSubmitProduct} className="grid gap-4 lg:grid-cols-12">
          <div className="lg:col-span-3">
            <Input
              label="Name"
              value={form.name}
              onChange={(e) => setForm((current) => ({ ...current, name: e.target.value }))}
              minLength={2}
              maxLength={150}
              required
              placeholder="Product name"
            />
          </div>
          <div className="lg:col-span-2">
            <Input
              label="Price"
              type="number"
              min="0.01"
              step="0.01"
              value={form.price}
              onChange={(e) => setForm((current) => ({ ...current, price: e.target.value }))}
              required
              placeholder="99.99"
            />
          </div>
          <div className="lg:col-span-2">
            <Input
              label="Stock"
              type="number"
              min="0"
              step="1"
              value={form.stock}
              onChange={(e) => setForm((current) => ({ ...current, stock: e.target.value }))}
              required
              placeholder="25"
            />
          </div>
          <label className="block lg:col-span-2">
            <span className="mb-1.5 block text-sm font-semibold text-slate-700">Category</span>
            {categories.length ? (
              <select
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                value={form.category_id}
                onChange={(e) => setForm((current) => ({ ...current, category_id: e.target.value }))}
                required
              >
                <option value="">Select category</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>{category.name}</option>
                ))}
              </select>
            ) : (
              <input
                className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                type="number"
                min="1"
                step="1"
                value={form.category_id}
                onChange={(e) => setForm((current) => ({ ...current, category_id: e.target.value }))}
                required
                placeholder="Category ID"
              />
            )}
          </label>
          <div className="lg:col-span-3">
            <Input
              label="Description"
              value={form.description}
              onChange={(e) => setForm((current) => ({ ...current, description: e.target.value }))}
              placeholder="Short description"
            />
          </div>
          <div className="flex flex-wrap gap-2 lg:col-span-12">
            <Button loading={saving}>
              {editingId ? <Save className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
              {editingId ? 'Update Product' : 'Add Product'}
            </Button>
            {editingId && (
              <Button type="button" variant="ghost" onClick={resetForm}>
                <X className="h-4 w-4" /> Cancel
              </Button>
            )}
          </div>
        </form>
      </Card>

      {loading ? <Loader /> : products.length === 0 ? <EmptyState title="No products found" /> : (
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAdd={handleAdd}
              onEdit={startEdit}
              onDelete={handleDelete}
              deleting={deletingId === product.id}
            />
          ))}
        </div>
      )}
    </section>
  );
};

export default ProductsPage;
