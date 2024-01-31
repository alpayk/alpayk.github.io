package com.gt.sample;

import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ProtocolException;
import java.net.Socket;
import java.net.URL;
import java.security.KeyManagementException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.Principal;
import java.security.PrivateKey;
import java.security.UnrecoverableEntryException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CountDownLatch;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.KeyManager;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import javax.net.ssl.TrustManagerFactory;
import javax.net.ssl.X509KeyManager;

public class TestClientmTLS {

	private static int THREAD_NUM = 1;
	private static int ITERATION_NUM = 1;
	private static CountDownLatch cdl;

	private static final String TRUSTSTORE_PASS = "123123";
	private static final String TRUSTSTORE_PATH = "truststore.jks";
	private static final String KEYSTORE_PASS = "123321";
	private static final String KEYSTORE_PATH = "9396e0f3-ba8f-42d6-bfde-072a3294ed15.jks";
	private static final int DEFAULT_BUFFER_SIZE = 4096;

	private static final String MTLS_TEST_URL = "https://mcustomers.garantibbva.com.tr/gbadsm/advanced-sign-mgmt-public/security-server-mtls/v1/mtlstesting";
	private static Random rand = new Random();
	private static List<String> aliases;

	private static String convertInputStreamToString(InputStream is) throws IOException {

		ByteArrayOutputStream result = new ByteArrayOutputStream();
		byte[] buffer = new byte[DEFAULT_BUFFER_SIZE];
		int length;
		while ((length = is.read(buffer)) != -1) {
			result.write(buffer, 0, length);
		}

		return result.toString("UTF-8");
	}

	public static String getRandAlias() {
		try {
			int rnd = rand.nextInt(aliases.size());
			return aliases.get(rnd);
		} catch (Exception e) {
			System.err.println(e);
			return null;
		}
	}

	public static void main(String[] args) {
		if (args.length > 0) {
			try {
				THREAD_NUM = Integer.parseInt(args[0]);
				ITERATION_NUM = Integer.parseInt(args[1]);
			} catch (Exception e) {
				System.out.println("Usage: TestClientmTLS <ThreadNum> <IterationNum>");
				return;
			}
		}

		cdl = new CountDownLatch(ITERATION_NUM * THREAD_NUM);

		long programStartTime = System.nanoTime();
		try {
			KeyStore keyStore = KeyStore.getInstance("JKS");
			FileInputStream fileInputStream = new FileInputStream(KEYSTORE_PATH);
			String password = KEYSTORE_PASS;
			keyStore.load(fileInputStream, password.toCharArray());

			aliases = Collections.list(keyStore.aliases());

			KeyStore trustStore = KeyStore.getInstance("JKS");
			trustStore.load(new FileInputStream(TRUSTSTORE_PATH), TRUSTSTORE_PASS.toCharArray());

			TrustManagerFactory trustManagerFactory = TrustManagerFactory
					.getInstance(TrustManagerFactory.getDefaultAlgorithm());
			trustManagerFactory.init(trustStore);

			TrustManager[] trustManagers = trustManagerFactory.getTrustManagers();

			URL url = new URL(MTLS_TEST_URL);

			for (int i = 0; i < THREAD_NUM; i++) {
				new Thread(new Runnable() {
					@Override
					public void run() {
						for (int j = 0; j < ITERATION_NUM; j++) {
							try {
								cdl.countDown();
								makeReq(keyStore, password, trustManagers, url);
							} catch (Exception e) {
								e.printStackTrace();
							}
						}
					}
				}).start();
			}
		} catch (IOException | KeyStoreException | NoSuchAlgorithmException | CertificateException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		}
		try {
			cdl.await();
			System.out.println("TotalTime: " + ((System.nanoTime() - programStartTime) / 1000000.0)
					+ "ms\nAvgRespTime: "
					+ ((System.nanoTime() - programStartTime) / 1000000.0) / (THREAD_NUM * ITERATION_NUM) + "ms");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private static void makeReq(KeyStore keyStore, String password, TrustManager[] trustManagers, URL url)
			throws NoSuchAlgorithmException, UnrecoverableEntryException, KeyStoreException, KeyManagementException,
			IOException, ProtocolException {
		KeyStore.PrivateKeyEntry privateKeyEntry = (KeyStore.PrivateKeyEntry) keyStore.getEntry(getRandAlias(),
				new KeyStore.PasswordProtection(password.toCharArray()));

//		System.out.println(privateKeyEntry.getCertificate().getPublicKey());
		PrivateKey privateKey = privateKeyEntry.getPrivateKey();

		SSLContext sslContext = SSLContext.getInstance("TLS");
		sslContext.init(
				new KeyManager[] { new KeyManagerImpl(privateKey, (X509Certificate) privateKeyEntry.getCertificate()) },
				trustManagers, null);

		SSLSocketFactory sslSocketFactory = sslContext.getSocketFactory();

		HttpsURLConnection connection = (HttpsURLConnection) url.openConnection();

		connection.setSSLSocketFactory(sslSocketFactory);
		connection.setRequestMethod("POST");

		int responseCode = connection.getResponseCode();
		System.out.println("HTTPCode: " + responseCode);
		if (responseCode == HttpsURLConnection.HTTP_OK) {
			InputStream responseStream = connection.getInputStream();
//			System.out.println(convertInputStreamToString(responseStream));
			responseStream.close();
		} else {
			InputStream errorStream = connection.getErrorStream();
//			System.err.println(convertInputStreamToString(errorStream));
			errorStream.close();
		}
	}

	private static class KeyManagerImpl implements X509KeyManager {
		private final PrivateKey privateKey;
		private final X509Certificate certificate;

		public KeyManagerImpl(PrivateKey privateKey, X509Certificate certificate) {
			this.privateKey = privateKey;
			this.certificate = certificate;
		}

		@Override
		public String chooseClientAlias(String[] keyType, Principal[] issuers, Socket socket) {
			return "";
		}

		@Override
		public X509Certificate[] getCertificateChain(String alias) {
			return new X509Certificate[] { certificate };
		}

		@Override
		public PrivateKey getPrivateKey(String alias) {
			return privateKey;
		}

		@Override
		public String chooseServerAlias(String keyType, Principal[] issuers, Socket socket) {
			// TODO Auto-generated method stub
			return null;
		}

		@Override
		public String[] getServerAliases(String keyType, Principal[] issuers) {
			// TODO Auto-generated method stub
			return null;
		}

		@Override
		public String[] getClientAliases(String keyType, Principal[] issuers) {
			// TODO Auto-generated method stub
			return null;
		}

	}
}