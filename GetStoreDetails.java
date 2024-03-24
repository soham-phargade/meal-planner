import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class GetStoreDetails {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://apimdev.wakefern.com/mockexample/V1/getStoreDetails"))
                .header("Ocp-Apim-Subscription-Key", "4ae9400a1eda4f14b3e7227f24b74b44")
                .header("Content-Type", "application/json")
                .GET() // GET is the default, but explicitly stated here for clarity.
                .build();

        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200) {
                // Define the file path where you want to save the output
                String filePath = "storeDetails.txt";
                // Write the response body to the file
                Files.writeString(Paths.get(filePath), response.body());
                System.out.println("Store details successfully written to " + filePath);
            } else {
                System.out.println("Failed to fetch data: " + response.statusCode());
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}

