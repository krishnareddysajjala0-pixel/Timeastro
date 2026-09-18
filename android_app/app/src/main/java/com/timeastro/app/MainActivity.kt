package com.timeastro.app

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.os.Bundle
import android.content.Context
import android.print.PrintAttributes
import android.print.PrintManager
import android.webkit.JavascriptInterface
import android.webkit.GeolocationPermissions
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private val LOCATION_PERMISSION_REQUEST_CODE = 1001

    inner class WebAppInterface {
        @JavascriptInterface
        fun printPage() {
            runOnUiThread {
                try {
                    val printManager = getSystemService(Context.PRINT_SERVICE) as PrintManager
                    val jobName = "RavanAstro_Kundali"
                    val printAdapter = webView.createPrintDocumentAdapter(jobName)
                    printManager.print(jobName, printAdapter, PrintAttributes.Builder().build())
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }

        @JavascriptInterface
        fun sharePdfData(base64Data: String, fileName: String) {
            runOnUiThread {
                try {
                    val cleanBase64 = if (base64Data.contains(",")) {
                        base64Data.substringAfter(",")
                    } else {
                        base64Data
                    }
                    val pdfBytes = android.util.Base64.decode(cleanBase64, android.util.Base64.DEFAULT)
                    val pdfFile = java.io.File(cacheDir, if (fileName.isEmpty()) "RavanAstro_Kundali.pdf" else fileName)
                    pdfFile.writeBytes(pdfBytes)

                    val uri = androidx.core.content.FileProvider.getUriForFile(
                        this@MainActivity,
                        "${packageName}.fileprovider",
                        pdfFile
                    )
                    val shareIntent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
                        type = "application/pdf"
                        putExtra(android.content.Intent.EXTRA_STREAM, uri)
                        addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                    startActivity(android.content.Intent.createChooser(shareIntent, "Share Kundali PDF..."))
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }

        @JavascriptInterface
        fun sharePdf() {
            printPage()
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize Python runtime if not started
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        // Create WebView UI
        webView = WebView(this)
        setContentView(webView)

        // Show immediate loading screen instead of black screen
        val loadingHtml = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        background-color: #121212;
                        color: #ffffff;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .spinner {
                        border: 4px solid rgba(255,255,255,0.1);
                        width: 48px;
                        height: 48px;
                        border-radius: 50%;
                        border-left-color: #ff9800;
                        animation: spin 1s linear infinite;
                        margin-bottom: 20px;
                    }
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    h2 { font-weight: 500; font-size: 20px; margin: 0; }
                </style>
            </head>
            <body>
                <div class="spinner"></div>
                <h2>Loading Timeastro...</h2>
            </body>
            </html>
        """.trimIndent()
        webView.loadDataWithBaseURL(null, loadingHtml, "text/html", "UTF-8", null)

        // Start embedded Flask server in background thread
        val py = Python.getInstance()
        val pyModule = py.getModule("server_launcher")
        
        Thread {
            try {
                pyModule.callAttr("start_server")
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()

        // Request runtime location permissions on app launch
        requestLocationPermission()

        val settings: WebSettings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.allowFileAccess = true
        settings.setGeolocationEnabled(true)

        webView.addJavascriptInterface(WebAppInterface(), "AndroidPrint")

        webView.webChromeClient = object : WebChromeClient() {
            override fun onGeolocationPermissionsShowPrompt(
                origin: String?,
                callback: GeolocationPermissions.Callback?
            ) {
                callback?.invoke(origin, true, false)
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                if (request?.isForMainFrame == true) {
                    view?.postDelayed({
                        view.loadUrl("http://127.0.0.1:5000")
                    }, 500)
                }
            }
        }

        // Poll local port and load server once ready
        pollAndLoadServer()
    }

    private fun requestLocationPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION),
                LOCATION_PERMISSION_REQUEST_CODE
            )
        }
    }

    private fun pollAndLoadServer() {
        Thread {
            var connected = false
            var attempts = 0
            while (!connected && attempts < 60) {
                try {
                    val socket = java.net.Socket("127.0.0.1", 5000)
                    socket.close()
                    connected = true
                } catch (e: Exception) {
                    attempts++
                    Thread.sleep(500)
                }
            }
            runOnUiThread {
                webView.loadUrl("http://127.0.0.1:5000")
            }
        }.start()
    }

    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}

