USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_Dates]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_Dates](
	[VGProductID] [int] NOT NULL,
	[RegistrationBegins] [smalldatetime] NULL,
	[BiddingBegins] [datetime] NULL,
	[LastDepositDate] [smalldatetime] NULL,
	[LastCertDepositDate] [smalldatetime] NULL,
	[BiddingEnds] [smalldatetime] NULL,
	[TaxSaleDate] [smalldatetime] NULL,
	[LastPayDate] [smalldatetime] NULL,
	[RegistrationDeadline] [smalldatetime] NULL
) ON [PRIMARY]
GO
