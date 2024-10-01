---
title: "Modded YouTube App"
date: 2024-06-01
draft: false
description: "Open-source YouTube tweaks for iOS to improve the experience"
tags: ["open source", "pull requests", "issue tracking", "feature requests", "objective-c", "swift"]
---

## What is it

I've recently been contributing to a few different open-source projects for creating modified YouTube apps for iOS. These projects allow you to modify your YouTube app to have improved functionality, including new buttons, new controls, and many new options.

## Project 1: uYouEnhanced https://github.com/arichornlover/uYouEnhanced

## Project 2: YTLitePlus https://github.com/YTLitePlus/YTLitePlus

## Things I've developed

### Suggested Video Removal

My first tweak that I developed back in January was a way to remove the suggested video popup that appears when completing a video. Below is an example of what this popup looks like:

![Suggested Video Popup](suggested%20video%20before.jpg)

I wrote this as a standalone tweak and posted it to GitHub here: [github.com/bhackel/ytnosuggestedvideo](https://github.com/bhackel/ytnosuggestedvideo). The code for this tweak looks pretty straightforward:

```obj-c
%group YTNSV_Tweak
// Overwrite the method that checks if the endscreen should be shown
%hook YTMainAppVideoPlayerOverlayViewController
- (bool)shouldShowAutonavEndscreen {
    if (IS_TWEAK_ENABLED) {
        return false;
    }
    return %orig;
}
%end
%end
```

It simply modifies the `shouldShowAutonavEndscreen` method of the `YTMainAppVideoPlayerOverlayViewController` class to return false when the tweak is enabled. However, getting to this point taught me a lot about how to use tools like Flipboard Explorer (FLEX) to dig through the class structure of the YouTube app and reverse-engineer the code that controls this popup.

After enabling this tweak, the popup is removed:

![Suggested Video Removed](suggested%20video%20after.jpg)

### Tap to Seek

One of the first feature requests I received was to add the Tap to Seek gesture present in Android into the iOS app. This gesture allows you to tap anywhere on the seek bar to immediately jump to that point in the video. At this point in my development journey, I learned that the jailbreak tweak development sphere, specifically with YouTube, is very gatekeep-ey. I found few guides for how to accomplish anything. Therefore, I decided to document my learning process on the GitHub readme in hopes that someone would find it in the future as something helpful for their own tweaks: [github.com/bhackel/yttaptoseek](https://github.com/bhackel/yttaptoseek)

![Tap to Seek](tap%20to%20seek.gif)

### In-App Player

Another feature request that I worked on was an in-app video player. Some other YouTube tweaks allow for downloading YouTube videos, and this feature complements that by allowing the user to play any video in the YouTube app using the native Apple video player.

![In-app Video Player](video%20player.gif)

### Player Gestures

The most recent project that I have undertaken is the development of gesture controls for the video player. This includes horizontal sliding gestures for controlling volume, brightness, and seeking. My goal with this feature was to focus on customizability and documentation. I wrote the code with a policy of over-commenting everything, so that a future developer could learn from my struggles when they create their own tweaks.

![Gesture Settings](gesture%20settings.jpg)

<details>
    <summary>Show Gesture Code</summary>

Feel free to judge my code

```obj-c
// Gestures - @bhackel
%group gPlayerGestures
%hook YTWatchLayerViewController
// invoked when the player view controller is either created or destroyed
- (void)watchController:(YTWatchController *)watchController didSetPlayerViewController:(YTPlayerViewController *)playerViewController {
    if (playerViewController) {
        // check to see if the pan gesture is already created
        if (!playerViewController.YTLitePlusPanGesture) {
            playerViewController.YTLitePlusPanGesture = [[UIPanGestureRecognizer alloc] initWithTarget:playerViewController
                                                                                               action:@selector(YTLitePlusHandlePanGesture:)];
            playerViewController.YTLitePlusPanGesture.delegate = playerViewController;
            [playerViewController.playerView addGestureRecognizer:playerViewController.YTLitePlusPanGesture];
        }        
    }
    %orig;
}
%end


%hook YTPlayerViewController
// the pan gesture that will be created and added to the player view
%property (nonatomic, retain) UIPanGestureRecognizer *YTLitePlusPanGesture;
/**
  * This method is called when the pan gesture is started, changed, or ended. It handles
  * 12 different possible cases depending on the configuration: 3 zones with 4 choices
  * for each zone. The zones are horizontal sections that divide the player into
  * 3 equal parts. The choices are volume, brightness, seek, and disabled.
  * There is also a deadzone that can be configured in the settings.
  * There are 4 logical states: initial, changed in deadzone, changed, end.
  */
%new
- (void)YTLitePlusHandlePanGesture:(UIPanGestureRecognizer *)panGestureRecognizer {
    // Haptic feedback generator
    static UIImpactFeedbackGenerator *feedbackGenerator;
    // Variables for storing initial values to be adjusted
    static float initialVolume;
    static float initialBrightness;
    static CGFloat initialTime;
    // Flag to determine if the pan gesture is valid
    static BOOL isValidHorizontalPan = NO;
    // Variable to store the section of the screen the gesture is in
    static GestureSection gestureSection = GestureSectionInvalid;
    // Variable to track the start location of the whole pan gesture
    static CGPoint startLocation;
    // Variable to track the X translation when exiting the deadzone
    static CGFloat deadzoneStartingXTranslation;
    // Variable to track the X translation of the pan gesture after exiting the deadzone
    static CGFloat adjustedTranslationX;
    // Variable used to smooth out the X translation
    static CGFloat smoothedTranslationX = 0;
    // Constant for the filter constant to change responsiveness
    // static const CGFloat filterConstant = 0.1;
    // Constant for the deadzone radius that can be changed in the settings
    static CGFloat deadzoneRadius = (CGFloat)GetFloat(@"playerGesturesDeadzone");
    // Constant for the sensitivity factor that can be changed in the settings
    static CGFloat sensitivityFactor = (CGFloat)GetFloat(@"playerGesturesSensitivity");
    // Objects for modifying the system volume
    static MPVolumeView *volumeView;
    static UISlider *volumeViewSlider;
    // Get objects that should only be initialized once
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        volumeView = [[MPVolumeView alloc] init];
        for (UIView *view in volumeView.subviews) {
            if ([view isKindOfClass:[UISlider class]]) {
                volumeViewSlider = (UISlider *)view;
                break;
            }
        }
        feedbackGenerator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleMedium];
    });
    // Get objects used to seek nicely in the video player
    static YTMainAppVideoPlayerOverlayViewController *mainVideoPlayerController = (YTMainAppVideoPlayerOverlayViewController *)self.childViewControllers.firstObject;
    static YTPlayerBarController *playerBarController = mainVideoPlayerController.playerBarController;
    static YTInlinePlayerBarContainerView *playerBar = playerBarController.playerBar;

/***** Helper functions for adjusting player state *****/
    // Helper function to adjust brightness
    void (^adjustBrightness)(CGFloat, CGFloat) = ^(CGFloat translationX, CGFloat initialBrightness) {
        float brightnessSensitivityFactor = 3;
        float newBrightness = initialBrightness + ((translationX / 1000.0) * sensitivityFactor * brightnessSensitivityFactor);
        newBrightness = fmaxf(fminf(newBrightness, 1.0), 0.0);
        [[UIScreen mainScreen] setBrightness:newBrightness];
    };

    // Helper function to adjust volume
    void (^adjustVolume)(CGFloat, CGFloat) = ^(CGFloat translationX, CGFloat initialVolume) {
        float volumeSensitivityFactor = 3.0;
        float newVolume = initialVolume + ((translationX / 1000.0) * sensitivityFactor * volumeSensitivityFactor);
        newVolume = fmaxf(fminf(newVolume, 1.0), 0.0);
        // Improve smoothness - ignore if the volume is within 0.01 of the current volume
        CGFloat currentVolume = [[AVAudioSession sharedInstance] outputVolume];
        if (fabs(newVolume - currentVolume) < 0.01 && currentVolume > 0.01 && currentVolume < 0.99) {
            return;
        }
        // https://stackoverflow.com/questions/50737943/how-to-change-volume-programmatically-on-ios-11-4
        
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(0.01 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            volumeViewSlider.value = newVolume;
        });
    };

    // Helper function to adjust seek time
    void (^adjustSeek)(CGFloat, CGFloat) = ^(CGFloat translationX, CGFloat initialTime) {
        // Get the location in view for the current video time
        CGFloat totalTime = self.currentVideoTotalMediaTime;
        CGFloat videoFraction = initialTime / totalTime;
        CGFloat initialTimeXPosition = [playerBar scrubXForScrubRange:videoFraction];
        // Calculate the new seek X position
        CGFloat sensitivityFactor = 1; // Adjust this value to make seeking more/less sensitive
        CGFloat newSeekXPosition = initialTimeXPosition + translationX * sensitivityFactor;
        // Create a CGPoint using this new X position
        CGPoint newSeekPoint = CGPointMake(newSeekXPosition, 0);
        // Send this to a seek method in the player bar controller
        [playerBarController didScrubToPoint:newSeekPoint];
    };

    // Helper function to smooth out the X translation
    // CGFloat (^applyLowPassFilter)(CGFloat) = ^(CGFloat newTranslation) {
    //     smoothedTranslationX = filterConstant * newTranslation + (1 - filterConstant) * smoothedTranslationX;
    //     return smoothedTranslationX;
    // };

/***** Helper functions for running the selected gesture *****/
    // Helper function to run any setup for the selected gesture mode
    void (^runSelectedGestureSetup)(NSString*) = ^(NSString *sectionKey) {
        // Determine the selected gesture mode using the section key
        GestureMode selectedGestureMode = (GestureMode)GetInteger(sectionKey);
        // Handle the setup based on the selected mode
        switch (selectedGestureMode) {
            case GestureModeVolume:
                initialVolume = [[AVAudioSession sharedInstance] outputVolume];
                break;
            case GestureModeBrightness:
                initialBrightness = [UIScreen mainScreen].brightness;
                break;
            case GestureModeSeek:
                initialTime = self.currentVideoMediaTime;
                // Start a seek action
                [playerBarController startScrubbing];
                break;
            case GestureModeDisabled:
                // Do nothing if the gesture is disabled
                break;
            default:
                // Show an alert if the gesture mode is invalid
                UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"Invalid Gesture Mode" message:@"Please report this bug." preferredStyle:UIAlertControllerStyleAlert];
                UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil];
                [alertController addAction:okAction];
                [self presentViewController:alertController animated:YES completion:nil];
                break;
        }
    };
    
    // Helper function to run the selected gesture action when the gesture changes
    void (^runSelectedGestureChanged)(NSString*) = ^(NSString *sectionKey) {
        // Determine the selected gesture mode using the section key
        GestureMode selectedGestureMode = (GestureMode)GetInteger(sectionKey);
        // Handle the gesture action based on the selected mode
        switch (selectedGestureMode) {
            case GestureModeVolume:
                adjustVolume(adjustedTranslationX, initialVolume);
                break;
            case GestureModeBrightness:
                adjustBrightness(adjustedTranslationX, initialBrightness);
                break;
            case GestureModeSeek:
                adjustSeek(adjustedTranslationX, initialTime);
                break;
            case GestureModeDisabled:
                // Do nothing if the gesture is disabled
                break;
            default:
                // Show an alert if the gesture mode is invalid
                UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"Invalid Gesture Mode" message:@"Please report this bug." preferredStyle:UIAlertControllerStyleAlert];
                UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil];
                [alertController addAction:okAction];
                [self presentViewController:alertController animated:YES completion:nil];
                break;
        }
    };

    // Helper function to run the selected gesture action when the gesture ends
    void (^runSelectedGestureEnded)(NSString*) = ^(NSString *sectionKey) {
        // Determine the selected gesture mode using the section key
        GestureMode selectedGestureMode = (GestureMode)GetInteger(sectionKey);
        // Handle the gesture action based on the selected mode
        switch (selectedGestureMode) {
            case GestureModeVolume:
                break;
            case GestureModeBrightness:
                break;
            case GestureModeSeek:
                [playerBarController endScrubbingForSeekSource:0];
                break;
            case GestureModeDisabled:
                break;
            default:
                // Show an alert if the gesture mode is invalid
                UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"Invalid Gesture Mode" message:@"Please report this bug." preferredStyle:UIAlertControllerStyleAlert];
                UIAlertAction *okAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault handler:nil];
                [alertController addAction:okAction];
                [self presentViewController:alertController animated:YES completion:nil];
                break;
        }
    };
/***** End of Helper functions *****/

    // Handle gesture based on current gesture state
    if (panGestureRecognizer.state == UIGestureRecognizerStateBegan) {
        // Get the gesture's start position
        startLocation = [panGestureRecognizer locationInView:self.view];
        CGFloat viewHeight = self.view.bounds.size.height;
        // Determine the section based on the start position by dividing the view into thirds
        if (startLocation.y <= viewHeight / 3.0) {
            gestureSection = GestureSectionTop;
        } else if (startLocation.y <= 2 * viewHeight / 3.0) {
            gestureSection = GestureSectionMiddle;
        } else if (startLocation.y <= viewHeight) {
            gestureSection = GestureSectionBottom;
        } else {
            gestureSection = GestureSectionInvalid;
        }
        // Cancel the gesture if the chosen mode for this section is disabled
        if (       ((gestureSection == GestureSectionTop)    && (GetInteger(@"playerGestureTopSelection")    == GestureModeDisabled))
                || ((gestureSection == GestureSectionMiddle) && (GetInteger(@"playerGestureMiddleSelection") == GestureModeDisabled))
                || ((gestureSection == GestureSectionBottom) && (GetInteger(@"playerGestureBottomSelection") == GestureModeDisabled))) {
            panGestureRecognizer.state = UIGestureRecognizerStateCancelled;
            return;
        }
        // Deactive the activity flag
        isValidHorizontalPan = NO;
        // Cancel this gesture if it has not activated after 1 second
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(1 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            if (!isValidHorizontalPan && panGestureRecognizer.state != UIGestureRecognizerStateEnded) {
                // Cancel the gesture by setting its state to UIGestureRecognizerStateCancelled
                panGestureRecognizer.state = UIGestureRecognizerStateCancelled;
            }
        });
    }

    // Handle changed gesture state by activating the gesture once it has exited the deadzone,
    // and then adjusting the player based on the selected gesture mode
    if (panGestureRecognizer.state == UIGestureRecognizerStateChanged) {
        // Determine if the gesture is predominantly horizontal
        CGPoint translation = [panGestureRecognizer translationInView:self.view];
        if (!isValidHorizontalPan) {
            if (fabs(translation.x) > fabs(translation.y)) {
                // Check if the touch has moved outside the deadzone
                CGFloat distanceFromStart = hypot(translation.x, translation.y);
                if (distanceFromStart < deadzoneRadius) {
                    // If within the deadzone, don't activate the pan gesture
                    return;
                }
                // If outside the deadzone, activate the pan gesture and store the initial values
                isValidHorizontalPan = YES;
                deadzoneStartingXTranslation = translation.x;
                adjustedTranslationX = 0;
                smoothedTranslationX = 0;
                // Run the setup for the selected gesture mode
                switch (gestureSection) {
                    case GestureSectionTop:
                        runSelectedGestureSetup(@"playerGestureTopSelection");
                        break;
                    case GestureSectionMiddle:
                        runSelectedGestureSetup(@"playerGestureMiddleSelection");
                        break;
                    case GestureSectionBottom:
                        runSelectedGestureSetup(@"playerGestureBottomSelection");
                        break;
                    default:
                        // If the section is invalid, cancel the gesture
                        panGestureRecognizer.state = UIGestureRecognizerStateCancelled;
                        break;
                }
                // Provide haptic feedback to indicate a gesture start
                if (IS_ENABLED(@"playerGesturesHapticFeedback_enabled")) {
                    [feedbackGenerator prepare];
                    [feedbackGenerator impactOccurred];
                }
            } else {
                // Cancel the gesture if the translation is not horizontal
                panGestureRecognizer.state = UIGestureRecognizerStateCancelled;
                return;
            }
        }
        
        // Handle the gesture based on the identified section
        if (isValidHorizontalPan) {
            // Adjust the X translation based on the value hit after exiting the deadzone
            adjustedTranslationX = translation.x - deadzoneStartingXTranslation;
            // Smooth the translation value
            // adjustedTranslationX = applyLowPassFilter(adjustedTranslationX);
            // Pass the adjusted translation to the selected gesture
            switch (gestureSection) {
                case GestureSectionTop:
                    runSelectedGestureChanged(@"playerGestureTopSelection");
                    break;
                case GestureSectionMiddle:
                    runSelectedGestureChanged(@"playerGestureMiddleSelection");
                    break;
                case GestureSectionBottom:
                    runSelectedGestureChanged(@"playerGestureBottomSelection");
                    break;
                default:
                    // If the section is invalid, cancel the gesture
                    panGestureRecognizer.state = UIGestureRecognizerStateCancelled;
                    break;
            }
        }
    }

    // Handle the gesture end state by running the selected gesture mode's end action
    if (panGestureRecognizer.state == UIGestureRecognizerStateEnded && isValidHorizontalPan) {
        switch (gestureSection) {
            case GestureSectionTop:
                runSelectedGestureEnded(@"playerGestureTopSelection");
                break;
            case GestureSectionMiddle:
                runSelectedGestureEnded(@"playerGestureMiddleSelection");
                break;
            case GestureSectionBottom:
                runSelectedGestureEnded(@"playerGestureBottomSelection");
                break;
            default:
                break;
        }
        // Provide haptic feedback upon successful gesture recognition
        // [feedbackGenerator prepare];
        // [feedbackGenerator impactOccurred];
    }

}
// allow the pan gesture to be recognized simultaneously with other gestures
%new
- (BOOL)gestureRecognizer:(UIGestureRecognizer *)gestureRecognizer shouldRecognizeSimultaneouslyWithGestureRecognizer:(UIGestureRecognizer *)otherGestureRecognizer {
    if ([gestureRecognizer isKindOfClass:[UIPanGestureRecognizer class]] && [otherGestureRecognizer isKindOfClass:[UIPanGestureRecognizer class]]) {
        // Do not allow this gesture to activate with the normal seek bar gesture
        YTMainAppVideoPlayerOverlayViewController *mainVideoPlayerController = (YTMainAppVideoPlayerOverlayViewController *)self.childViewControllers.firstObject;
        YTPlayerBarController *playerBarController = mainVideoPlayerController.playerBarController;
        YTInlinePlayerBarContainerView *playerBar = playerBarController.playerBar;
        if (otherGestureRecognizer == playerBar.scrubGestureRecognizer) {
            return NO;
        }
        // Do not allow this gesture to activate with the fine scrubber gesture
        YTFineScrubberFilmstripView *fineScrubberFilmstrip = playerBar.fineScrubberFilmstrip;
        if (!fineScrubberFilmstrip) {
            return YES;
        }
        YTFineScrubberFilmstripCollectionView *filmstripCollectionView = [fineScrubberFilmstrip valueForKey:@"_filmstripCollectionView"];
        if (filmstripCollectionView && otherGestureRecognizer == filmstripCollectionView.panGestureRecognizer) {
            return NO;
        }

    }
    return YES;
}
%end
%end
```

</details>

## Things I've managed

Along with all of the tweaks that I have developed, I've also gained a lot of experience working with other developers in an open-source environment. I involved myself throughout the whole development pipeline: creating a useful issue template, replying and solving issues, closing feature requests with pull requests, creating releases, and talking to users about where they want the project to go.

I've also participated in a Telegram group for discussing the project and helping users build the app for themselves. I try to be friendly and welcoming since, like many large open-source projects, users can be hard to work with sometimes.

## Why I'm no longer contributing

I've recently decided to stop development of this project. This is partially because I realized the implications of working on a tool that allows one to violate YouTube's terms of service by blocking ads. Additionally, I know that this will negatively impact creators by preventing them from earning ad revenue.

My main goal when I started working on this project was to remove all suggested videos from my feed, and I have successfully done that. This reduces the likelihood of being stuck in brain rot by watching recommended videos. I feel like it allows me to be more free from the mental manipulation of modern social media. I stick to watching only my subscriptions, which have a set amount of uploads per day. 