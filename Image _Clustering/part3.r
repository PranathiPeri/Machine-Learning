library(jpeg)
library(ggplot2)

#Image 1
img <- readJPEG ("C:/Users/perip/Downloads/ML/HomeWork/Assignment6/Part3/image1.jpg")
direct = "C:/Users/perip/Downloads/ML/HomeWork/Assignment6/Part3"
sub_direct = "clustered_images"
imgDm <- dim(img)  # Obtaining the image dimension

imgRGB <- data.frame(
  x = rep(1:imgDm[2], each = imgDm[1]),
  y = rep(imgDm[1]:1, imgDm[2]),
  R = as.vector(img[,,1]),
  G = as.vector(img[,,2]),
  B = as.vector(img[,,3])
)

kClusters <- 2
kMeans <- kmeans(imgRGB[, c("R", "G", "B")], centers = kClusters)
kColours <- rgb(kMeans$centers[kMeans$cluster,])

ggp<-ggplot(data = imgRGB, aes(x = x, y = y)) + 
  geom_point(colour = kColours) +
  labs(title = paste("k-Means Clustering of", kClusters, "Colours")) +
  xlab("x") +
  ylab("y") 
dir.create(file.path(direct,sub_direct),showWarnings = FALSE)
setwd(file.path(direct,sub_direct))
ggsave(ggp, file = "image1_10.jpg") 

#Image 2

img <- readJPEG ("C:/Users/perip/Downloads/ML/HomeWork/Assignment6/Part3/image2.jpg")


imgDm <- dim(img)  # Obtaining the image dimension

imgRGB <- data.frame(
  x = rep(1:imgDm[2], each = imgDm[1]),
  y = rep(imgDm[1]:1, imgDm[2]),
  R = as.vector(img[,,1]),
  G = as.vector(img[,,2]),
  B = as.vector(img[,,3])
)


kClusters <- 5
kMeans <- kmeans(imgRGB[, c("R", "G", "B")], centers = kClusters)
kColours <- rgb(kMeans$centers[kMeans$cluster,])


ggp<-ggplot(data = imgRGB, aes(x = x, y = y)) + 
  geom_point(colour = kColours) +
  labs(title = paste("k-Means Clustering of", kClusters, "Colours")) +
  xlab("x") +
  ylab("y") 

ggsave(ggp, file = "image2_5.jpg") 


#Image 3
img <- readJPEG ("C:/Users/perip/Downloads/ML/HomeWork/Assignment6/Part3/image5.jpg")


imgDm <- dim(img)  # Obtaining the image dimension

imgRGB <- data.frame(
  x = rep(1:imgDm[2], each = imgDm[1]),
  y = rep(imgDm[1]:1, imgDm[2]),
  R = as.vector(img[,,1]),
  G = as.vector(img[,,2]),
  B = as.vector(img[,,3])
)


kClusters <- 5
kMeans <- kmeans(imgRGB[, c("R", "G", "B")], centers = kClusters)
kColours <- rgb(kMeans$centers[kMeans$cluster,])


ggp<-ggplot(data = imgRGB, aes(x = x, y = y)) + 
  geom_point(colour = kColours) +
  labs(title = paste("k-Means Clustering of", kClusters, "Colours")) +
  xlab("x") +
  ylab("y") 

ggsave(ggp, file = "image5_5.jpg") 

