import FileUpload from './components/FileUpload';

const [result, setResult] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);

const handleUpload = async (file) => {
  setLoading(true);
  setError(null);
  try {
    const data = await uploadInvoice(file);
    setResult(data);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

function App() {
  return (
    <div className='min-h-screen bg-gray-50'>
      <header className='bg-white shadow'>
        <div className='max-w-7xl mx-auto py-4 px-6'>
          <h1 className='text-2xl font-bold text-gray-900'>AI Invoice Parser</h1>
          <p className='text-gray-500'>Upload invoices → Extract data with AI</p>
        </div>
      </header>

      <main className='max-w-7xl mx-auto py-8 px-6'>
        <div className='bg-white rounded-lg shadow p-8 text-center text-gray-400'>
          <FileUpload onUpload={(file) => console.log('Uploaded file:', file)} />
        </div>
      </main>
    </div>
  );
}

export default App;
