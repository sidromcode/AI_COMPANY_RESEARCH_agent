import React from 'react';
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }
    static getDerivedStateFromError(error) {
        return { hasError: true };
    }
    componentDidCatch(error, errorInfo) {
        this.setState({ error, errorInfo });
        console.error("Uncaught error:", error, errorInfo);
    }
    render() {
        if (this.state.hasError) {
            return (
                <div className="h-screen w-screen bg-slate-900 text-white p-10 flex flex-col items-center justify-center gap-4">
                    <h1 className="text-2xl font-bold text-red-400">Something went wrong.</h1>
                    <div className="bg-black/50 p-4 rounded-lg max-w-2xl overflow-auto font-mono text-xs text-slate-300">
                        <p className="mb-2 text-red-300">{this.state.error && this.state.error.toString()}</p>
                        <pre>{this.state.errorInfo && this.state.errorInfo.componentStack}</pre>
                    </div>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-4 py-2 bg-indigo-600 rounded-lg hover:bg-indigo-500 transition-colors"
                    >
                        Reload Application
                    </button>
                </div>
            );
        }
        return this.props.children;
    }
}
export default ErrorBoundary;