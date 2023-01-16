package client;

import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Reader;
import java.io.Writer;
import java.security.cert.Certificate;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Client1 {

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

	public static SSLSocket createSocket(String host, int port) throws IOException {
		SSLSocket socket = (SSLSocket) SSLSocketFactory.getDefault()
				.createSocket(host, port);
		socket.setNeedClientAuth(true);
		socket.setEnabledProtocols(protocols);
		socket.setEnabledCipherSuites(cipher_suites);
		return socket;
	}

	public static void main(String[] args) throws Exception {
		System.setProperty("javax.net.ssl.keyStore", "C:\\Programming\\jdk-16\\lib\\security\\serverkeystore.jks");
		System.setProperty("javax.net.ssl.keyStorePassword", "changeit");
		System.setProperty("javax.net.ssl.trustStore", "C:\\Programming\\jdk-16\\lib\\security\\serverkeystore.jks");
		System.setProperty("javax.net.ssl.trustStorePassword", "changeit");

		try (SSLSocket socket = createSocket("bnr.ro", 443)) {
			Reader in = new InputStreamReader(socket.getInputStream());
			Writer out = new OutputStreamWriter(socket.getOutputStream());

			// Builder request header
			out.write("GET /Home.aspx HTTP/1.1\r\n");
			out.write("Host: bnr.ro\r\n");
			out.write("User-Agent: Mozilla/5.0\r\n");
			out.write("Accept: text/xml,application/xml,application/xhtml+xml,text/html*/*\r\n");
			out.write("Accept-Language: en-us\r\n");
			out.write("Accept-Charset: ISO-8859-1,utf-8\r\n");
			out.write("Connection: keep-alive\r\n");
			out.write("\r\n");
			out.flush();

			char[] data = new char[10240];
			int len = in.read(data);
			if (len <= 0) {
				throw new IOException("Error: No data received!");
			}

			String[] lines = (new String(data, 0, len)).split("\r\n");
			String header = Arrays.stream(lines).limit(9).collect(Collectors.joining("\r\n"));
			String body = Arrays.stream(lines).skip(11).collect(Collectors.joining("\r\n"));

			// Save response header
			try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr.header"))) {
				writer.write(header);
			}

			// Save response body
			try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr.html"))) {
				writer.write(body);
			}

			// Fishing certificate information
			Certificate certificate = socket.getSession().getPeerCertificates()[0];
			String[] cert_body = certificate.toString().split("\n");
			String versionNumber = cert_body[2].split(": ")[1];
			String serialNumber = cert_body[13].replaceAll("[ \\[\\]]", "").split(":")[1];
			String issuer = cert_body[12].split(": ")[1];
			String validFrom = cert_body[10].replaceAll("[\\[,]", "").split(": ")[2];
			String validTo = cert_body[11].replaceAll("[\\]]", "").split(": ")[1];
			String subject = cert_body[3].split(": ")[1];
			String publicKey = certificate.getPublicKey().toString();

			// Printing out the gathered information
			System.out.printf("Version: %s%n", versionNumber);
			System.out.printf("Serial: %s%n", serialNumber);
			System.out.printf("Issuer: %s%n", issuer);
			System.out.printf("Valid from: %s%n", validFrom);
			System.out.printf("Valid to: %s%n", validTo);
			System.out.printf("Subject: %s%n", subject);
			System.out.printf("Public key:%n  %s%n", publicKey);
		}
	}
}
