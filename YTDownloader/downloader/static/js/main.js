$(document).ready(function () {
    // Toastr options
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    // Show loader
    function showLoader() {
        $("#loaderOverlay").fadeIn();
        $("#loader").show();
    }

    // Hide loader
    function hideLoader() {
        $("#loaderOverlay").fadeOut();
        $("#loader").hide();
    }

    // Validate Link
    function validateLink(link) {
        function isValidYouTubeLink(singleLink) {
            const ytRegex = /^https:\/\/www\.youtube\.com\/watch\?v=.+/;
            return ytRegex.test(singleLink);
        }

        if (Array.isArray(link)) {
            if (link.length === 0) {
                toastr.error("Please enter at least one link.");
                return false;
            }
            for (let i = 0; i < link.length; i++) {
                if (!isValidYouTubeLink(link[i])) {
                    toastr.error("Please enter valid YouTube links.");
                    return false;
                }
            }
        } else {
            if (!link) {
                toastr.error("Please enter a link.");
                return false;
            } else if (!isValidYouTubeLink(link)) {
                toastr.error("Please enter a valid YouTube link.");
                return false;
            }
        }

        return true;
    }

    // Trigger download
    function downloadFile(filename) {
        var downloadUrl = "download_video";  
        let csrfmiddlewaretoken = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            url: downloadUrl,
            type: 'POST',
            data: JSON.stringify({ "filename": filename }),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': csrfmiddlewaretoken },
            xhrFields: {
                responseType: 'blob'
            },
            success: function (response, status, xhr) {
                var blob = new Blob([response], { type: xhr.getResponseHeader('Content-Type') });
                var downloadUrl = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(downloadUrl);
            },
            error: function (xhr, status, error) {
                toastr.error("Failed to download the file: " + error);
            }
        });
        return true;
    }


    // Form submission
    $("#DownloadSingleForm").submit(function (e) {
        e.preventDefault();
        let link = $("#link").val();
        let token = $('input[name="csrfmiddlewaretoken"]').val();
        let resolution = $("#resolution").val();

        let links = link.split(',').map(l => l.trim());

        for (let i = 0; i < links.length; i++) {
            if (links[i] === "")
                links = "";
        }
        let formData = {
            link: JSON.stringify(links),
            resolution: resolution,
            csrfmiddlewaretoken: token
        }

        if (validateLink(links)) {
            showLoader();
            $.ajax({
                url: "/download",
                type: "POST",

                data: formData,
                success: function (response) {
                    hideLoader();
                    $("#link").val("");
                    if (response.status) {
                        Swal.fire({
                            title: "Success",
                            text: "Video(s) downloaded successfully!",
                            icon: "success",
                            showCancelButton: true,
                            confirmButtonText: 'Download',
                            cancelButtonText: 'Close'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                if (response.file_type === 1){
                                    if (downloadFile(response.zip_file_name)){
                                        toastr.success("File downloaded successfully.");
                                    }
                                }
                                else {
                                    if (downloadFile(response.file_name)){
                                        toastr.success("File downloaded successfully.");
                                    }
                                }
                                
                            }
                        });
                    } else {
                        toastr.error(response.msg);
                    }
                },
                error: function () {
                    hideLoader();
                    toastr.error("An error occurred while downloading the video(s).");
                }
            });
        }
    });
});
