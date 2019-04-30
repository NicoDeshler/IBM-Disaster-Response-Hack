
% Google Maps image data directories.
satImgDir = fullfile('Test\satellite\');
mapImgDir = fullfile('Test\map');


% Instantiate image data store.
satImgs = imageDatastore(satImgDir);
satImgs.ReadFcn = @rgbImgReader;
mapImgs = imageDatastore(mapImgDir);

trainingSet_Size = numel(satImgs.Files);

% Generate Low/Med/High Disaster Rating Training Sets
for i = 1:trainingSet_Size
    sat_raw = Crop_Icon(readimage(satImgs, i));
    map_raw = Crop_Icon(readimage(mapImgs, i));
    
    disaster_level =  mod(i,3) + 1;
    nominal_sat_roads = Isolate_Roads(sat_raw, map_raw);
    
    disaster_sat_roads = Gaussian_Noise(nominal_sat_roads, disaster_level);
    disaster_impact = nominal_sat_roads - disaster_sat_roads; 
    imwrite(disaster_impact, [int2str(disaster_level),'_Level', '\', 'data', int2str(i), '.png'])
        
end
    
 %% Simulated Training Data Example:
%{ 
n = 98;
sat_raw = Crop_Icon(readimage(satImgs, n));
map_raw = Crop_Icon(readimage(mapImgs, n));

nominal_sat_roads = Isolate_Roads(sat_raw, map_raw);
disaster_sat_roads = Gaussian_Noise(nominal_sat_roads, 'high');
disaster_impact = nominal_sat_roads - disaster_sat_roads; 

subplot(2,2,1);
title('Satellite Image');
imshow(sat_raw)

subplot(2,2,2);
imshow(map_raw==max(map_raw(:)))
title('Road Map Image')

subplot(2,2,3);
imshow(disaster_sat_roads)
title('Satellite Image Road Isolation')

subplot(2,2,4);
imshow(disaster_impact)
title('Simulated Disaster Effects')
%}


function roads = Isolate_Roads(sat_raw, map_raw)
% Isolates Roads by applying a thresholded map view image mask on the
% satellite view image. 
road_binary = double(repmat(Road_Mask(map_raw),1,1,3));
roads = sat_raw.*road_binary;

end

function mask = Road_Mask(map_raw)
% Generate road binary from Google Maps map view image.

% Extract the individual red, green, and blue color channels.
redChannel = map_raw(:, :, 1);
%greenChannel = map_raw(:, :, 2);
%blueChannel = map_raw(:, :, 3);

% Find white, where each color channel is more than 250
thresholdValue = max(map_raw(:));
mask = redChannel >= thresholdValue-1;
%mask = redChannel > thresholdValue & greenChannel > thresholdValue & blueChannel > thresholdValue;

end

% Add gaussian noise to the roads based on the disaster intensity
% classification.
function noisy_road = Gaussian_Noise(road_nominal, disaster_rating)
m = mean(road_nominal(:));

% Blur variance determined based on disaster level
switch (disaster_rating)
    case 1
        gauss_var = m;
    case 2
        gauss_var = m*10;
    case 3
        gauss_var = m*100;
end

% Apply gaussian noise to image
noise = double(imnoise(zeros(size(road_nominal)), 'gaussian', 1, gauss_var));
noisy_road = road_nominal.*noise;
end

function cImg = Crop_Icon(img)
    c = 50;
    cImg = img(1:end-c,:,:);
end

function data = rgbImgReader(filename)
    [im,cmap] = imread(filename);
    data = ind2rgb(im,cmap);
end







