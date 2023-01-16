package server;

import javax.net.ServerSocketFactory;
import javax.net.ssl.SSLServerSocket;
import javax.net.ssl.SSLServerSocketFactory;
import javax.net.ssl.SSLSocket;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;

public class Server2 {

	private static final String[] protocols = new String[] {"TLSv1.2"};
	private static final String[] cipher_suites = new String[] {
			"TLS_DHE_DSS_WITH_AES_256_CBC_SHA256",
			"TLS_AES_128_GCM_SHA256",
			"TLS_AES_256_GCM_SHA384",
			"TLS_CHACHA20_POLY1305_SHA256",
			"TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
			"TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
			"TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
			"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
			"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
			"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
			"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
			"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
			"TLS_RSA_WITH_AES_128_GCM_SHA256",
			"TLS_RSA_WITH_AES_256_GCM_SHA384",
			"TLS_RSA_WITH_AES_128_CBC_SHA",
			"TLS_RSA_WITH_AES_256_CBC_SHA"
	};

	public static void main(String[] args) throws IOException {
		System.setProperty("javax.net.ssl.keyStore", "C:\\Programming\\jdk-16\\lib\\security\\serverkeystore.jks");
		System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
		System.setProperty("javax.net.ssl.trustStore", "C:\\Programming\\jdk-16\\lib\\security\\serverkeystore.jks");
		System.setProperty("javax.net.ssl.trustStorePassword", "changeit");

		ServerSocketFactory factory = SSLServerSocketFactory.getDefault();
		try (SSLServerSocket sslListener = (SSLServerSocket) factory.createServerSocket(443)) {
			sslListener.setNeedClientAuth(true);
			sslListener.setEnabledProtocols(protocols);
			sslListener.setEnabledCipherSuites(cipher_suites);

			try (
					SSLSocket socket = (SSLSocket) sslListener.accept();
			        BufferedReader reader1 = new BufferedReader(new FileReader("bnr_server.header"));
			        BufferedReader reader2 = new BufferedReader(new FileReader("bnr_server.html"))
			) {
				Writer out = new OutputStreamWriter(socket.getOutputStream());
				char[] data = new char[10240];

				int len = reader1.read(data);
				out.write(data, 0, len);
				out.write("\r\n\r\n\r\n");
				len = reader2.read(data);
				out.write(data, 0, len);
				out.flush();
			}
		}
	}
}
