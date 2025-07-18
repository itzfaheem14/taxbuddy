import { AppProps } from 'next/app';
import Head from 'next/head';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/router';

// Global styles and theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#9c27b0', // Purple
      light: '#ba68c8',
      dark: '#7b1fa2',
    },
    secondary: {
      main: '#f50057', // Pink
      light: '#ff5983',
      dark: '#c51162',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0b0b0',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.5rem',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 25,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 15,
          background: 'linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(156, 39, 176, 0.2)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(26, 26, 26, 0.9)',
          backdropFilter: 'blur(10px)',
        },
      },
    },
  },
});

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Page transition variants
const pageVariants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  in: {
    opacity: 1,
    y: 0,
  },
  out: {
    opacity: 0,
    y: -20,
  },
};

const pageTransition = {
  type: 'tween',
  ease: 'anticipate',
  duration: 0.4,
};

function MuseAIkaApp({ Component, pageProps }: AppProps) {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <>
      <Head>
        <title>MuseAIka - AI-Powered Music Emotion Engine</title>
        <meta name="description" content="Discover music that matches your emotions with AI-powered facial recognition and sentiment analysis" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </Head>

      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={darkTheme}>
          <CssBaseline />
          
          {/* Global Styles */}
          <style jsx global>{`
            html {
              scroll-behavior: smooth;
            }
            
            body {
              background: linear-gradient(135deg, #0a0a0a 0%, #1a0a1a 50%, #0a0a1a 100%);
              background-attachment: fixed;
              min-height: 100vh;
            }

            /* Custom scrollbar */
            ::-webkit-scrollbar {
              width: 8px;
            }

            ::-webkit-scrollbar-track {
              background: rgba(26, 26, 26, 0.5);
            }

            ::-webkit-scrollbar-thumb {
              background: linear-gradient(45deg, #9c27b0, #f50057);
              border-radius: 4px;
            }

            ::-webkit-scrollbar-thumb:hover {
              background: linear-gradient(45deg, #ba68c8, #ff5983);
            }

            /* Glassmorphism effect */
            .glass {
              background: rgba(26, 26, 26, 0.7);
              backdrop-filter: blur(10px);
              border: 1px solid rgba(156, 39, 176, 0.2);
            }

            /* Glow effects */
            .glow {
              box-shadow: 0 0 20px rgba(156, 39, 176, 0.3);
            }

            .glow-pink {
              box-shadow: 0 0 20px rgba(245, 0, 87, 0.3);
            }

            /* Loading animation */
            @keyframes pulse {
              0%, 100% {
                opacity: 1;
              }
              50% {
                opacity: 0.5;
              }
            }

            .pulse {
              animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }

            /* Music visualization bars */
            @keyframes musicBars {
              0%, 100% {
                height: 20%;
              }
              50% {
                height: 100%;
              }
            }

            .music-bar {
              animation: musicBars 1s ease-in-out infinite;
            }

            .music-bar:nth-child(2) {
              animation-delay: 0.1s;
            }

            .music-bar:nth-child(3) {
              animation-delay: 0.2s;
            }

            .music-bar:nth-child(4) {
              animation-delay: 0.3s;
            }

            .music-bar:nth-child(5) {
              animation-delay: 0.4s;
            }
          `}</style>

          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={router.route}
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
            >
              <Component {...pageProps} />
            </motion.div>
          </AnimatePresence>

          {/* Global Toast Notifications */}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'rgba(26, 26, 26, 0.9)',
                color: '#fff',
                border: '1px solid rgba(156, 39, 176, 0.3)',
                backdropFilter: 'blur(10px)',
              },
              success: {
                iconTheme: {
                  primary: '#4caf50',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#f44336',
                  secondary: '#fff',
                },
              },
            }}
          />
        </ThemeProvider>
      </QueryClientProvider>
    </>
  );
}

export default MuseAIkaApp;