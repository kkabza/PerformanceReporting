USE [Taxsale2024]
GO
/****** Object:  StoredProcedure [dbo].[vg_RemovePendingBidderIDRequest]    Script Date: 3/31/2025 3:44:48 PM ******/
SET ANSI_NULLS OFF
GO
SET QUOTED_IDENTIFIER OFF
GO
CREATE PROCEDURE [dbo].[vg_RemovePendingBidderIDRequest] 
	@UserID uniqueidentifier,
	@VGProductID	int
	
AS
DELETE FROM vg_BidderNumbers
WHERE (UserId = @UserID) AND (VGProductID = @VGProductID) AND (BidderNumber = null)
GO
